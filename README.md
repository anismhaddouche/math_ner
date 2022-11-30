# Project Description
The purpose of this paper is to detect and measure collaborative writing strategies, between students, in the computer-supported collaborative learning environment [Labnbook](https://labnbook.fr) for the development of a text document. These strategies, defined in [onrubia2009strategies](https://psycnet.apa.org/record/2009-14113-001), are the sequential summative construction and the sequential integrating construction. To this end, we construct two indicators: the balance of contribution indicators and the co-writing indicator.

This project is decomposed in following three subprojects:
* train_ner: the goal is to create a named entity model with [SpaCy](https://spacy.io) in order to detect the position of mathematical equations in the text (see its readme). The train and dev corpus are, first, annotated automatically with some regular expressions (Regex).
* correct_ner: the aim here is to correct the model created in the train_ner subprojet by annotating or correcting the train and dev manually with [Prodigy](https://prodi.gy).
* indicators: in this subproject we use the output trained ner model of the subproject correct_ner to create the indicators introduced above. 

For more details, please refer to the README.md of each subproject. Note that, the subproject 'indicators' contains all materials needed to compute the above indicators. Note also, in order to install the virtual environment, named `labnbook`, used for this project please run the following command in your terminal. `conda env create -f path/to/environment.yml`


