Changelog
=========

3.1.0 (2022-07-13)
------------------

- Restore our css, so the background image is shown.  [maurits]

- Test with Plone 5.0, 5.1, 5.2 and 6.0.
  Test on all Python versions supported by Plone.  [maurits]


3.0.0 (2020-05-06)
------------------

- [chg] introduce breaking change removing dependency from collective.tiles.advancedstatic;
  also allow to use different registry field to store css syle
  [lucabel]


2.0.2 (2020-03-05)
------------------

- Run modernize, switched implements->implementer, remove AT reference.
  [pnicolli]

2.0.1 (2019-02-15)
------------------

- Avoid empty background image, that cause html page reload as image
  [mamico]


2.0.0 (2017-09-13)
------------------

- Drop Plone < 5 compatibility. For Plone < 5, use 1.x branch.
  [cekk]


1.4.1 (2017-01-11)
------------------

- Added compatibility with dexterity images used as background images [pnicolli]


1.4.0 (2016-02-26)
------------------

- Added option to open header and footer links in a new window [pnicolli]
- Added a title attribute to header and footer links for accessibility purposes [pnicolli]

1.3.4 (2016-02-24)
------------------

- Changed css rendering from "import" to "link" [pnicolli]
- Added target attribute to header and footer link [pnicolli]


1.3.3 (2014-12-11)
------------------

- Do not show portlet without border, if there isn't any text [cekk]


1.3.2 (2014-09-10)
------------------

- Moved to github [cekk]


1.3.1 (2013-01-25)
------------------

- Fix italian translation [mirco.angelini]


1.3.0 (2013-01-14)
------------------

- Fixed acquisition problem in getting background image [cekk]
- Added css stylesheet for background image [cekk]


1.2.5 (2012-07-25)
------------------

- Added dutch translations [maurits]


1.2.4 (2012-05-02)
------------------

- fixed Plone4 compatibility with hide field [cekk]


1.2.3 (2012-04-10)
------------------

- fixed default value for hide portlet field [cekk]

1.2.2 (2011-10-18)
------------------

- fixed Plone 4.1 compatibility in EditForm action [cekk]

1.2.1 (2011-10-13)
------------------

- fixed include permission to be Plone 4.1 compatible [mirco.angelini]

1.2.0 (2011-10-10)
------------------

- fixed vocabulary import to be Plone 4.1 compatible [keul]
- removed broken ram.cache in render [cekk]

1.1.5 (2011-09-05)
------------------
- new-old image workaround [mauro]
- omit-border version of the portlet wasn't using the portal transformed HTML [keul]

1.1.4 (2011-08-04)
------------------
- fixed compatibility between old version (1.0.4) and new header image management [cekk]

1.1.3 (2011-07-22)
------------------
- fixed text formatting and dependency with plone.portlet.static=1.2.1 [cekk]

1.1.2 (2011-07-18)
------------------
- fixed url generating [cekk]

1.1.1 (2011-07-13)
------------------
- fixed control in the footer [cekk]

1.1.0 (2011-06-30)
------------------

- now the images are references to an image in the site [cekk]
- release on pypi [cekk]

1.0.2 (2011-04-04)
------------------

- fixed bug in the path for internal links [cekk]

1.0.1 (2011-03-24)
------------------

- fixed problem with accents [cekk]

1.0.0 (2011-03-14)
------------------

- Initial release
