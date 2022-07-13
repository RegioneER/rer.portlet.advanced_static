from setuptools import setup, find_packages
import os

version = "3.1.0"

setup(
    name="rer.portlet.advanced_static",
    version=version,
    description="A portlet that extends Plone static text portlet, and add"
    " more functionalities",
    long_description=open("README.rst").read()
    + "\n"
    + open(os.path.join("docs", "HISTORY.rst")).read(),
    # Get more strings from http://pypi.org/classifiers/
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="portlet static",
    author="RedTurtle Technology",
    author_email="sviluppoplone@redturtle.net",
    url="http://plone.org/products/rer.portlet.advanced_static",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["rer", "rer.portlet"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "Products.CMFPlone",
        "plone.portlet.static>=1.2.1",
    ],
    extras_require=dict(test=["plone.app.testing", "plone.testing>=5.0.0"]),
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
