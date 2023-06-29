# Document Search Engine

Tools:
- Python
- HTML
- Flask
- AWS (EC2, DynamoDB)

About:

Created a search engine through Flask that would allow the user to input a series of words that would find the top 5 most relevant books that related to the input. The input would cleaned through tokenization and the removal of stopwords. Next, it would query the DynamoDB table for every book that contained the user's input and find the relevance score of each book. It would then output the top 5 books with the highest relevant scores in a table, showing the user which books are the most relevant to their specific input. 

![image](https://github.com/TitusGoh/Document-Search-Engine/assets/107716314/85ac51de-19e7-461c-95fb-0e93de0c97c5)

