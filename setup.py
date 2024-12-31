from setuptools import setup, find_packages

def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()

def read_file(file):
   with open(file) as f:
        return f.read()
    
long_description = read_file("README.md")
version = 1.0
requirements = read_requirements("requirements.txt")

setup(
    name = 'FasterAPI',
    version = version,
    author = 'emmaalaoui, brcpaul, enzomotariol',
    author_email = 'emma.alaoui-mhamdi@dauphine.eu, paul.bourcereau@dauphine.eu, enzo.montariol@gmail.com',
    description = 'A simple and fast API framework based on FastAPI.',
    long_description_content_type = "text/markdown", 
    long_description = long_description,
    license = "MIT license",
    packages = find_packages(exclude=["tests"]),
    install_requires = requirements,
)