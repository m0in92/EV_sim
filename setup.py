from distutils.core import setup


with open("README.md", 'r', encoding='utf8') as file:
    long_description = file.read()
    file.close()

setup(name='EV_sim',
      version='0.0.1',
      description="Electric Vehicle Dynamics Simulation Package",
      long_description=long_description,
      author="Moin Ahmed",
      author_email="moinahmed100#gmail.com",
      packages=["EV_sim"],
      install_requires=['numpy', 'pandas', 'matplotlib'],
      )