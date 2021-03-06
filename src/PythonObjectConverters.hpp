/*

 Copyright (c) 2005-2016, University of Oxford.
 All rights reserved.

 University of Oxford means the Chancellor, Masters and Scholars of the
 University of Oxford, having an administrative office at Wellington
 Square, Oxford OX1 2JD, UK.

 This file is part of Chaste.

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions are met:
 * Redistributions of source code must retain the above copyright notice,
 this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice,
 this list of conditions and the following disclaimer in the documentation
 and/or other materials provided with the distribution.
 * Neither the name of the University of Oxford nor the names of its
 contributors may be used to endorse or promote products derived from this
 software without specific prior written permission.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
 GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
 OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

 */

#ifndef PYTHONOBJECTCONVERTERS_HPP_
#define PYTHONOBJECTCONVERTERS_HPP_

#include <iostream>
#include <sstream>
#include <boost/python.hpp>
#include <boost/python/module.hpp>
#include <boost/python/stl_iterator.hpp>
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION //Ignore numpy depracated warnings
#include <numpy/ndarrayobject.h>
#define _BACKWARD_BACKWARD_WARNING_H 1 //Ignore vtk deprecated warnings
#include <vtkSmartPointer.h>
#include <vtkObjectBase.h>
#include "UblasIncludes.hpp"

using namespace boost::python;

/**
 *  This is a collection of converters of C++ to Python objects and Python to C++ objects.
 *  Some work is required to implement Chaste naming conventions, although I think some method names may
 *  need to follow boost conventions. Also definitions should be moved to a CPP file, although care is needed
 *  to make sure all necessary templated methods are instantiated.
 */

/**
 *  Convert VTK pointers to Python VTK objects, templated over vtk object type
 *  Source: http://www.vtk.org/Wiki/Example_from_and_to_python_converters
 */
template<class T>
struct VtkSmartPointerToPython
{
    /**
     *  Do the conversion
     *  @param rVtkSmartPointerToObject a vtk smart pointer
     *  @return A pointer to the Python object. Can be a None object if the smart pointer is empty.
     */
    static PyObject* convert(const vtkSmartPointer<T> &rVtkSmartPointer)
    {
        // Make sure something is being pointed to, otherwise return python None type
        if(rVtkSmartPointer.GetPointer() == NULL)
        {
            return incref(Py_None);
        }

        // Get the address string of the vtk object
        std::ostringstream oss;
        oss << (void*) rVtkSmartPointer.GetPointer();
        std::string address_str = oss.str();

        // Can get vtk object type from address string using vtk tricks
        boost::python::object obj = import("vtk").attr("vtkObjectBase")(address_str);

        // Important to increment object reference
        return incref(obj.ptr());
    }
};

/**
 *  Convert a Python VTK object to a pointer to the VTK object.
 *  Care is needed in suitably casting the returned void pointer to the desired
 *  vtk type. No checking is done here.
 *  Source: http://www.vtk.org/Wiki/Example_from_and_to_python_converters
 *  @param pPythonObject pointer to the python object
 *  @return void pointer to the vtk object
 */
void* ExtractVtkWrappedPointer(PyObject* pPythonObject)
{
    //Get the __this__ attribute from the Python Object
    char thisStr[] = "__this__";

    // Several checks to make sure it is a valid vtk type, otherwise return a null pointer
    if (!PyObject_HasAttrString(pPythonObject, thisStr))
    {
        return NULL;
    }

    PyObject* thisAttr = PyObject_GetAttrString(pPythonObject, thisStr);
    if (thisAttr == NULL)
    {
        return NULL;
    }

    const char* str = PyString_AsString(thisAttr);
    if(str == 0 || strlen(str) < 1)
    {
        return NULL;
    }

    char hex_address[32], *pEnd;
    const char *_p_ = strstr(str, "_p_vtk");
    if(_p_ == NULL)
    {
        return NULL;
    }

    const char *class_name = strstr(_p_, "vtk");
    if(class_name == NULL)
    {
        return NULL;

    }

    // Create a generic vtk object pointer and assign the address of the python object to it
    strcpy(hex_address, str+1);
    hex_address[_p_-str-1] = '\0';
    long address = strtol(hex_address, &pEnd, 16);

    vtkObjectBase* vtk_object = (vtkObjectBase*)((void*)address);
    if(vtk_object->IsA(class_name))
    {
        vtk_object->Register(NULL);
        return vtk_object;
    }

    // Catch all in case something goes wrong
    return NULL;
};

/**
 *  Convert a c_vector to a numpy array. Templated over c_vector type
 */
template<class T>
struct CVectorToNumpyArray
{
    /**
     *  Do the conversion
     *  @param rVector the c_vector to be converted
     *  @return a pointer to a numpy array
     */
    static PyObject* convert(T const& rVector)
    {
        // Convert to a double array
        npy_intp size = rVector.size();
        double * data = size ? const_cast<double *>(&rVector[0]) : static_cast<double *>(NULL);

        // Create a new numpy array and insert the data
        PyObject * pyObj = PyArray_SimpleNewFromData(1, &size, NPY_DOUBLE, data);
        boost::python::handle<> handle( pyObj );
        boost::python::numeric::array arr( handle );

        // Increment the reference count for the array
        return incref(arr.ptr());
    }
};

/**
 *  Convert a numpy array to a cvector, templated over the c_vector dimension
 *  If the numpy array is to small extra dimensions are zero padded. If it is too
 *  large extra dimensions are ignored.
 */
struct NumpyArrayToCVector
{
    template <unsigned DIM>
    NumpyArrayToCVector& from_python()
    {
        boost::python::converter::registry::push_back(&NumpyArrayToCVector::convertible,
                &NumpyArrayToCVector::construct<DIM>,
                boost::python::type_id<c_vector<double, DIM> >());
        return *this;
    }

    // Determine if a c_vector can be generated, otherwise return null
    static void* convertible(PyObject* pPythonObject)
    {
        if (PyArray_Check(pPythonObject))
        {
            PyArrayObject* arrayObjPtr = reinterpret_cast<PyArrayObject*>(pPythonObject);
            if(PyArray_NDIM(arrayObjPtr) == 1)
            {
                return pPythonObject;
            }
        }
        return NULL;
    }

    // Do the conversion
    template <unsigned DIM>
    static void construct(PyObject* pPythonObject, boost::python::converter::rvalue_from_python_stage1_data* data)
    {
        // Set up the c_vector
        typedef boost::python::converter::rvalue_from_python_storage<c_vector<double, DIM> > storage_type;
        void* storage = reinterpret_cast<storage_type*>(data)->storage.bytes;
        new (storage) c_vector<double, DIM>;
        c_vector<double, DIM>* vec = (c_vector<double, DIM>*) storage;

        // Populate the vector, fill unused dimensions with 0, excess dimensions are ignored
        PyArrayObject* arrayObjPtr = reinterpret_cast<PyArrayObject*>(pPythonObject);
        int size_array = PyArray_DIM(arrayObjPtr, 0);
        for(unsigned idx = 0; idx<DIM; idx++)
        {
            if(idx < unsigned(size_array))
            {
                (*vec)[idx] = extract<double>(PyArray_GETITEM(arrayObjPtr, (const char*)PyArray_GETPTR1(arrayObjPtr, idx)));
            }
            else
            {
                (*vec)[idx] = 0.0;
            }
        }
        data->convertible = storage;
    }
};

/**
 *  Convert a Python tuple to a cvector
 *  If the tuple is too small extra dimensions are zero padded. If it is too
 *  large extra dimensions are ignored.
 */
struct TupleToCVector
{
    template <unsigned DIM>
    TupleToCVector& from_python()
    {
        boost::python::converter::registry::push_back(&TupleToCVector::convertible,
                &TupleToCVector::construct<DIM>,
                boost::python::type_id<c_vector<double, DIM> >());
        return *this;
    }

    static void* convertible(PyObject* pPythonObject)
    {
        if (PyTuple_Check(pPythonObject))
        {
            return pPythonObject;
        }
        return NULL;
    }

    // Do the conversion
    template <unsigned DIM>
    static void construct(PyObject* pPythonObject, boost::python::converter::rvalue_from_python_stage1_data* data)
    {
        typedef boost::python::converter::rvalue_from_python_storage<c_vector<double, DIM> > storage_type;
        void* storage = reinterpret_cast<storage_type*>(data)->storage.bytes;
        new (storage) c_vector<double, DIM>;
        c_vector<double, DIM>* vec = (c_vector<double, DIM>*) storage;

        // Populate the vector
        int tuple_size = PyTuple_Size(pPythonObject);
        for(unsigned idx = 0; idx<DIM; idx++)
        {
            if(idx < unsigned(tuple_size))
            {
                (*vec)[idx] = extract<double>(PyTuple_GetItem(pPythonObject, idx));;
            }
            else
            {
                (*vec)[idx] = 0.0;
            }
        }
        data->convertible = storage;
    }
};

/**
 *  Convert a vector of quantities castable to double to a numpy array
 *  @param T the cvector type
 */
template<class T>
struct StdVectorToNumpyArray
{
    static PyObject* convert(T const& rVector)
    {
        npy_intp size = rVector.size();
        double * data = size ? const_cast<double *>(&rVector[0]) : static_cast<double *>(NULL);
        PyObject * pyObj = PyArray_SimpleNewFromData(1, &size, NPY_DOUBLE, data);
        boost::python::handle<> handle( pyObj );
        boost::python::numeric::array arr( handle );
        return incref(arr.ptr());
    }
};

/**
 * Convert STL Iterators to Python Iterators
 */
template <class Container>
class vector_ptr_indexing_suite : public vector_indexing_suite<Container, true, vector_ptr_indexing_suite<Container> >
{
public:

    template <class Class>
    static void extension_def(Class & cl)
    {
        vector_indexing_suite<Container, true, vector_ptr_indexing_suite<Container> >::extension_def(cl);
        cl.def("__iter__", iterator<Container, return_value_policy<copy_non_const_reference> >());
    }
};


/**
 * Convert Python Iterables to C++
 *
 */
struct PythonIterableToStl
{

    template <typename Container>
    PythonIterableToStl&
    from_python()
    {
        boost::python::converter::registry::push_back(
                &PythonIterableToStl::convertible,
                &PythonIterableToStl::construct<Container>,
                boost::python::type_id<Container>());

        // Support chaining.
        return *this;
    }

    // Check if PyObject is iterable.
    static void* convertible(PyObject* object)
    {
        return PyObject_GetIter(object) ? object : NULL;
    }

    template <typename Container>
    static void construct(PyObject* object, boost::python::converter::rvalue_from_python_stage1_data* data)
    {
        namespace python = boost::python;
        python::handle<> handle(python::borrowed(object));

        typedef python::converter::rvalue_from_python_storage<Container> storage_type;
        void* storage = reinterpret_cast<storage_type*>(data)->storage.bytes;
        typedef python::stl_input_iterator<typename Container::value_type>iterator;

        new (storage) Container(
                iterator(python::object(handle)), // begin
                iterator());// end
        data->convertible = storage;
    }
};

#endif /*PYTHONOBJECTCONVERTERS_HPP_*/
