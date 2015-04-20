********************
quintagroup.substyle
********************
*Styles for site subsections.*

.. image:: https://travis-ci.org/quintagroup/quintagroup.substyle.png
       :target: https://travis-ci.org/quintagroup/quintagroup.substyle

.. image:: https://saucelabs.com/buildstatus/q-substyle
       :target: https://saucelabs.com/u/q-substyle

Introduction
============

Several Plone themes developed by Quintagroup feature different color schemes that can be set not only for the whole website, but also for any of its subsections. These themes are: `Flow <http://themes.quintagroup.com/product/flow>`_, `Berry <http://themes.quintagroup.com/product/berry>`_, `Wink <http://themes.quintagroup.com/product/wink>`_, `Business4 <http://themes.quintagroup.com/product/business4>`_, and `Chameleon <http://themes.quintagroup.com/product/chameleon>`_. Using quintagroup.substyle users can customize site section and change the default theme colors according to their specific wishes. For the themes that do not include color schemes out of the box you can add styles for site subsections manually.

Installation
============

Find your **buildout.cfg** file and add quintagroup.substyle to the eggs section of your buildout::

   [buildout]
   ...
   eggs =
      ...
      quintagroup.substyle

Rerun the buildout and restart your Zope instance.

Usage
=====

1. Activate quintagroup.substyle product via **Site Setup** > **Add-ons**. 
2. Navigate to the content item you want to change the colors for and open **Set Style** tab.
3. Fill in the offered fields according to the theme-specific instructions (insert either theme’s color scheme or a valid CSS color): 

    `Flow <http://quintagroup.com/services/support/tutorials/flow-skin/diazo/color-scheme/>`_ 

    `Berry <http://quintagroup.com/services/support/tutorials/berry-theme/theme-colours/part-4-how-to-set-theme-colours>`_ 

    `Wink <http://quintagroup.com/services/support/tutorials/wink-theme/set-theme-colors/part-3-how-to-set-theme-colours>`_ 

    `Business4 <http://quintagroup.com/services/support/tutorials/business4-theme/diazo/color>`_

    `Chameleon <http://quintagroup.com/services/support/tutorials/chameleon-skin/diazo/color-scheme>`_


4. Save changes after you are done and see the new theme colors in the current site section. Depending on the Plone theme you have installed, top image, portlet, carousel and whole section background color will be changed. If you edited styles for a folder, its contents will inherit new color scheme.

quintagroup.substyle can be used for other themes but you will need to customize template in site_properties:

1. Add **/portal_properties/site_properties** to your website’s URL. 
2. Add new properties (enter a name, type and value for the new property and click the "**Add**" button): 

**customsubstyles** - lines type - field name:title:description (e.g. backgroundcolor:Background color:background color)

**substyleshelp** - string - description of the tab (e.g. You can change theme colors on different site sections.)

**substylestemplate** - string - template (use `template-strings format <https://docs.python.org/2/library/string.html#template-strings>`_, e.g..documentFirstHeading {background-color: $backgroundcolor;}\n#portal-top {background-color: $backgroundcolor;})

.. image:: http://quintagroup.com/services/plone-development/products/quintagroup.substyle/add-substyle.png
       :target: http://quintagroup.com/services/plone-development/products/quintagroup.substyle

.. image:: http://quintagroup.com/services/plone-development/products/quintagroup.substyle/set-style-with-quintagroup-substyle.png
       :target: http://quintagroup.com/services/plone-development/products/quintagroup.substyle

Supported Plone versions:
-------------------------
- Plone 4.3
- Plone 4.2
- Plone 4.1
- Plone 4
- Plone 3
