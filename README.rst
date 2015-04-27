Lyvi
====

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/ok100/lyvi?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

For more information, see http://ok100.github.io/lyvi/


You can install the python dependencies by issuing:

.. code-block:: python

    $ sudo pip install -r pip_requirements.txt --use-mirrors

This will also be done for you when issuing the setup.py script.

There are other dependencies that need to be installed separately though:

    * ``libglyr`` (https://github.com/sahib/glyr)

For MPRIS support these dependencies are needed:

    * ``python-dbus``
    * ``python-gobject``
On OS X homebrew:
    *``python-dbus``
    *``pygobject``

Chances are that all these are available by your package manager.
