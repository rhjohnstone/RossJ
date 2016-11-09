# RossJ

This is a Chaste project, originally based on James Grogran's [PyChaste](https://github.com/jmsgrogan/PyChaste) project. The idea is to wrap solving of action potential models (done by Chaste) in Python to make MCMC easier by passing vectors of parameter values all over the place.

The RossJ project code needs to be included in the `projects` folder of the main Chaste source. This can be done with a symbolic link:

```bash
cd $CHASTE_SOURCE_DIR/projects
ln -s $PYCHASTE_PROJECT_SOURCE_DIR
```

or just by copying the project in. To build, create a build directory outside the source tree and proceed as:

```bash
cd $BUILD_DIR
cmake $CHASTE_SOURCE_DIR
make project_PyChaste
make project_PyChaste_Python
``` 

## Usage

I haven't messed around with adding anything to the PYTHONPATH yet.

The package can be imported in Python as normal. For example, in a Python session do:

```python
>>> import rossj
>>> ross = rossj.RossManual("hello")
>>> print rossj.GetMessage()

hello
```
