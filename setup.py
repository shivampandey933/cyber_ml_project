from setuptools import setup, find_packages


def get_requirements(file_path:str) -> list[str]:
    requirements=[]
    try:

        with open(file_path) as file:
           requirements=file.readlines()
           requirements=[req.replace("\n","") for req in requirements]
           if "-e ." in requirements:
            requirements.remove("-e .")
    except FileNotFoundError:
           raise FileNotFoundError("Requirements.txt file not found")        
    return requirements
    



setup(
    name="Network_security",
    version="0.0.1",
    author="Shivam Pandey",
    author_mail="pandeyshivam8765@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("Requirements.txt")
)