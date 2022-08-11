## Métriques de classification : 
* Matrice de confusion :
    - TP : prédiction dans la classe et réalité dans la classe aussi 
    - TN : Prédiction en dehors de la classe et réalité aussi 
    - FN : Prédiction n'est pas dans la classe et la réalité est dans la classe
    - FP : Prédiction dans la classe et réalité pas dans la classe
* Précision 
    - Nombre d'entités correctement attribués à la classe (TP) / Nombre d'entités attribués à cette classe pour (TP + FP)
    - Elle permet de connaître le nombre de prédictions positifs bien effectuées
    - Plus la Precision est haute, moins le modèle se trompe sur les positifs
* Rappel
    - Nombre d'entités correctement attribués à la classe (TP) / Nombre d'entités appartenant à cette classe pour (TP + FN)
    - Permet de savoir le pourcentage de positifs bien prédit par notre modèle.
    - Plus le Rappel est haut, plus le modèle repère de positif
* F1 score:
    - Moyenne harmonique entre rappel et precision :
    $\frac{2}{1/rappel + 1/precision}$


## A faire : 
* Pour la segmentation en phrase : 
    * Extraire les délimiteur de phrase du code php "<p>,<\p> et body ..."
    * Extraire le délimiteur de cellule dans les tables
    * Les remplacer par un nouveau symbole 
* Pour l'extraction d'entités nommés : 
    * Rajouter une nouvelle entité pour les valeur du type d=24kg pour les différencier des formules