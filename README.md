# pyAdmin
Python instance for administration of Testaments de Poilus platform

## Procédure d'import des données
- Ouvrir le fichier d'inventaire avec un logiciel tableur pour en vérifier le contenu
    - Identifier les images à retravailler à la main
    - Vérifier que le document ne contient aucun point-virgule
    - Sauvegarder les deux feuilles du tableur dans deux fichiers csv distincts, intitutilés **data-metadata.csv** et **data_numerisation.csv**
    - Lors de la conversion CSV, le délimiteur de champ doit être ";", il ne faut pas de délimiteur de texte et il faut exporter en UTF-8
    - Supprimer la première ligne (titre des champs) de chaque fichier
    - Vérifier que toutes les lignes soient bien formées (sur la même ligne)
    - Copier-coller les fichiers dans l'application Python, dans le dossier **importer/data**
- Faire un test d'upload sur la version test de l'application :
    - Vérifier que la ligne `read_data` (environ ligne 38) appelle les bons fichiers de metadonnées
    - Exécuter le fichier **dev_uploader.py**
- Si tout s'est bien passé en test, répéter l'opération avec le fichier **prod_uploader.py**