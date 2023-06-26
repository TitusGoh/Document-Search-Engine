from boto3.dynamodb.conditions import Key
from flask import Flask, render_template, request
import boto3
import re

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('tfidf')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    stopwords_set = set(["a", "as", "able", "about", "above", "according", "accordingly",
       "across", "actually", "after", "afterwards", "again", "against", "aint", "all", "allow",
       "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among",
       "amongst", "an", "and", "another", "any", "anybody", "anyhow", "anyone", "anything", "anyway",
       "anyways", "anywhere", "apart", "appear","appreciate", "appropriate", "are", "arent", "around",
       "as", "aside", "ask", "asking", "associated", "at", "available", "away", "awfully", "be", "became",
       "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "believe", "below",
       "beside", "besides", "best", "better", "between", "beyond", "both", "brief", "but", "by", "cmon",
       "cs", "came", "can", "cant", "cannot", "cant", "cause", "causes", "certain", "certainly", "changes",
       "clearly", "co", "com", "come", "comes", "concerning", "consequently", "consider", "considering", "contain", "containing",
       "contains", "corresponding", "could", "couldnt", "course", "currently", "definitely", "described", "despite", "did", "didnt",
       "different", "do", "does", "doesnt", "doing", "dont", "done", "down", "downwards", "during", "each",
       "edu", "eg", "eight", "either", "else", "elsewhere", "enough", "entirely", "especially", "et", "etc",
       "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except",
       "far", "few", "ff", "fifth", "first", "five", "followed", "following", "follows", "for", "former",
       "formerly", "forth", "four", "from", "further", "furthermore", "get", "gets", "getting", "given", "gives",
       "go", "goes", "going", "gone", "got", "gotten", "greetings", "had", "hadnt", "happens", "hardly",
       "has", "hasnt", "have", "havent", "having", "he", "hes", "hello", "help", "hence", "her",
       "here", "heres", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "hi", "him", "himself",
       "his", "hither", "hopefully", "how", "howbeit", "however", "i", "id", "ill", "im", "ive",
       "ie", "if", "ignored", "immediate", "in", "inasmuch", "inc", "indeed", "indicate", "indicated", "indicates",
       "inner", "insofar", "instead", "into", "inward", "is", "isnt", "it", "itd", "itll", "its",
       "its", "itself", "just", "keep", "keeps", "kept", "know", "knows", "known", "last", "lately",
       "later", "latter", "latterly", "least", "less", "lest", "let", "lets", "like", "liked", "likely",
       "little", "look", "looking", "looks", "ltd", "mainly", "many", "may", "maybe", "me", "mean",
       "meanwhile", "merely", "might", "more", "moreover", "most", "mostly", "much", "must", "my", "myself",
       "name", "namely", "nd", "near", "nearly", "necessary", "need", "needs", "neither", "never", "nevertheless",
       "new", "next", "nine", "no", "nobody", "non", "none", "noone", "nor", "normally", "not",
       "nothing", "novel", "now", "nowhere", "obviously", "of", "off", "often", "oh", "ok", "okay",
       "old", "on", "once", "one", "ones", "only", "onto", "or", "other", "others", "otherwise",
       "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "own", "particular", "particularly",
       "per", "perhaps", "placed", "please", "plus", "possible", "presumably", "probably", "provides", "que", "quite",
       "qv", "rather", "rd", "re", "really", "reasonably", "regarding", "regardless", "regards", "relatively", "respectively",
       "right", "said", "same", "saw", "say", "saying", "says", "second", "secondly", "see", "seeing",
       "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously",
       "seven", "several", "shall", "she", "should", "shouldnt", "since", "six", "so", "some", "somebody",
       "somehow", "someone", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specified", "specify",
       "specifying", "still", "sub", "such", "sup", "sure", "ts", "take", "taken", "tell", "tends",
       "th", "than", "thank", "thanks", "thanx", "that", "thats", "thats", "the", "their", "theirs",
       "them", "themselves", "then", "thence", "there", "theres", "thereafter", "thereby", "therefore", "therein", "theres",
       "thereupon", "these", "they", "theyd", "theyll", "theyre", "theyve", "think", "third", "this", "thorough",
       "thoroughly", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too",
       "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "twice", "two", "un",
       "under", "unfortunately", "unless", "unlikely", "until", "unto", "up", "upon", "us", "use", "used",
       "useful", "uses", "using", "usually", "value", "various", "very", "via", "viz", "vs", "want",
       "wants", "was", "wasnt", "way", "we", "wed", "well", "were", "weve", "welcome", "well",
       "went", "were", "werent", "what", "whats", "whatever", "when", "whence", "whenever", "where", "wheres",
       "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who",
       "whos", "whoever", "whole", "whom", "whose", "why", "will", "willing", "wish", "with", "within",
       "without", "wont", "wonder", "would", "would", "wouldnt", "yes", "yet", "you", "youd", "youll",
       "youre", "youve", "your", "yours", "yourself", "yourselves", "zero"])


    tokens = set()
    finalWords = []
    user_input = request.form['user_input'].strip()
    #tokenize input
    for word in user_input.strip().split():
        lower = word.lower()
        lower = lower.replace("_"," ")
        parts = re.findall(r'\w+', lower)
        for part in parts:
            tokens.add(part)
    #check if it is less t
    for token in tokens:
        if token not in stopwords_set and len(token) > 1 and not token.isdigit():
            finalWords.append(token)

    totalBooks = []
    #get all the results from the table
    for term in finalWords:
        response = table.query(KeyConditionExpression=Key('word').eq(term))
        totalBooks.extend(response['Items'])

    #sort books by book name
    sortedBooks = sorted(totalBooks, key = lambda x: x['book'])
    relevanceScore = {}
    docid = None
    #go through all the books
    for book in sortedBooks:
        #first run of the book, set the value to 0 in the dict
        if book['book'] != docid:
            relevanceScore[book['book']] = 0
        docid = book['book']
        tfidf = book['value']
        tfidf = float(tfidf)
        score = tfidf/len(finalWords)
        relevanceScore[docid] += score
    #get the top 5 highest scores
    answer = sorted(relevanceScore.items(), key = lambda x: x[1], reverse = True)[:5]
    #return to the html file with the table
    return render_template('output.html', data = answer)
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5330, debug=True)