Instagram DM helper (safe draft mode)
====================================

This utility helps analyze the first message from a DM conversation export and draft
an affectionate response for **human review**.

Important
---------

* It does not log in to Instagram.
* It does not send messages automatically.
* It is intended to keep interactions respectful and compliant.

Input format
------------

Provide a JSON file with a list of conversations:

.. code-block:: json

   [
     {
       "participant": "ana",
       "messages": [
         {"sender": "ana", "text": "Amei seus vídeos!", "timestamp": 1},
         {"sender": "saminho", "text": "Obrigada!", "timestamp": 2}
       ]
     }
   ]

Usage
-----

.. code-block:: bash

   python utils/instagram_dm_helper.py --input conversations.json --influencer saminho --seed 42
