
import nltk
import nltk.data
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import re
import spacy
import pandas as pd

nltk.download('averaged_perceptron_tagger')

nltk.download('punkt')

nlp = spacy.load('en_core_web_sm')
stemmer = LancasterStemmer()

sentences = []

# Dictionary to hold sentences corresponding to respective discourse markers
disc_sentences = {}

# Remaining sentences which do not have discourse markers (To be used later to generate other kinds of questions)
nondisc_sentences = []

# List of auxiliary verbs
aux_list = ['am', 'are', 'is', 'was', 'were', 'can', 'could', 'does', 'do', 'did', 'has', 'had', 'may', 'might', 'must',
            'need', 'ought', 'shall', 'should', 'will', 'would']

# List of all discourse markers
discourse_markers = ['because', 'as a result', 'since', 'when', 'although', 'for example', 'for instance']

# Different question types possible for each discourse marker
qtype = {'because': ['Why'], 'since': ['When', 'Why'], 'when': ['When'], 'although': ['Yes/No'], 'as a result': ['Why'], 
        'for example': ['Give an example where'], 'for instance': ['Give an instance where'], 'to': ['Why']}

# The argument which forms a question
target_arg = {'because': 1, 'since': 1, 'when': 1, 'although': 1, 'as a result': 2, 'for example': 1, 'for instance': 1, 
              'to': 1}

'''sentences = ['Our application proposes to create a full fledged tutorial given a text file ( Textbook chapters, pdf documents, etc) The tutorial will consist of short ppts/videos based on the text file given.',
 ' The text in the PPTs is summarised as required after text analysis and consists of the major points representing the topic of concern.',
 ' Audio explanation using voiceover is used to enhance comprehension of the user.',
 ' The entire application is enabled to support various Indian regional Languages to facilitate learning in language of choice providing language agnosticism.',
 ' In addition to this, assessments are provided after every subtopic to ensure user interaction.',
 ' The scores of the assessments and viewing activity is taken into account to provide a personalized progress tracker.',
 ' Multimedia inclusion in the tutorials is provided on the basis of the text analysed.',
 " A complete user friendly web interface is created for easy use of all the features and hassle free learning and customization based on the user's preferences.",
 ' This serves as an application for any kind of audience with an aim to learn something.']'''

def sentensify(data):
    global sentences
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    
    #data = '''Our application proposes to create a full fledged tutorial given a text file ( Textbook chapters, pdf documents, etc) The tutorial will consist of short ppts/videos based on the text file given. The text in the PPTs is summarised as required after text analysis and consists of the major points representing the topic of concern. Audio explanation using voiceover is used to enhance comprehension of the user. The entire application is enabled to support various Indian regional Languages to facilitate learning in language of choice providing language agnosticism. In addition to this, assessments are provided after every subtopic to ensure user interaction. The scores of the assessments and viewing activity is taken into account to provide a personalized progress tracker. Multimedia inclusion in the tutorials is provided on the basis of the text analysed.'''
    sentences = tokenizer.tokenize(data)
    return discourse()

def generate_question(question_part, type):

    ''' 
        question_part -> Part of input sentence which forms a question
        type-> The type of question (why, where, etc)
    '''
    # Remove full stop and make first letter lower case
    question_part = question_part[0].lower() + question_part[1:]
    if(question_part[-1] == '.' or question_part[-1] == ','):
        question_part = question_part[:-1]
        
    # Capitalizing 'i' since 'I' is recognized by parsers appropriately    
    for i in range(0, len(question_part)):
        if(question_part[i] == 'i'):
            if((i == 0 and question_part[i+1] == ' ') or (question_part[i-1] == ' ' and question_part[i+1] == ' ')):
                question_part = question_part[:i] + 'I' + question_part[i + 1: ]
                
    question = ""
    if(type == 'Give an example where' or type == 'Give an instance where'):
        question = type + " " + question_part + '?'
        return question

    aux_verb = False
    res = None
    
    # Find out if auxiliary verb already exists
    for i in range(len(aux_list)):
        if(aux_list[i] in question_part.split()):
            aux_verb = True
            pos = i
            break

    # If auxiliary verb exists
    if(aux_verb):
        
        # Tokeninze the part of the sentence from which the question has to be made
        text = nltk.word_tokenize(question_part)
        tags = nltk.pos_tag(text)
        question_part = ""
        fP = False
        
        for word, tag in tags:
            if(word in ['I', 'We', 'we']):
                question_part += 'you' + " "
                fP = True
                continue
            question_part += word + " "

        # Split across the auxiliary verb and prepend it at the start of question part
        question = question_part.split(" " + aux_list[pos])
        if(fP):
             question = ["were "] + question
        else:
            question = [aux_list[pos] + " "] + question

        # If Yes/No, no need to introduce question phrase
        if(type == 'Yes/No'):
            question += ['?']
            
        elif(type != "non_disc"):
            question = [type + " "] + question + ["?"]
            
        else:
            question = question + ["?"]
         
        question = ''.join(question)

    # If auxilary verb does ot exist, it can only be some form of verb 'do'
    else:
        aux = None
        text = nltk.word_tokenize(question_part)
        tags = nltk.pos_tag(text)
        comb = ""

        '''There can be following combinations of nouns and verbs:
            NN/NNP and VBZ  -> Does
            NNS/NNPS(plural) and VBP -> Do
            NN/NNP and VBN -> Did
            NNS/NNPS(plural) and VBN -> Did
        '''
        
        for tag in tags:
            if(comb == ""):
                if(tag[1] == 'NN' or tag[1] == 'NNP'):
                    comb = 'NN'

                elif(tag[1] == 'NNS' or tag[1] == 'NNPS'):
                    comb = 'NNS'

                elif(tag[1] == 'PRP'):
                    if tag[0] in ['He','She','It']:
                        comb = 'PRPS'
                    else:
                        comb = 'PRPP'
                        tmp = question_part.split(" ")
                        tmp = tmp[1: ]
                        if(tag[0] in ['I', 'we', 'We']):
                            question_part = 'you ' + ' '.join(tmp)
                            
            if(res == None):
                res = re.match(r"VB*", tag[1])
                if(res):
                    
                    # Stem the verb
                    question_part = question_part.replace(tag[0], stemmer.stem(tag[0]))
                res = re.match(r"VBN", tag[1])
                res = re.match(r"VBD", tag[1])

        if(comb == 'NN'):
            aux = 'does'
            
        elif(comb == 'NNS'):
            aux = 'do'
            
        elif(comb == 'PRPS'):
            aux = 'does'
            
        elif(comb == 'PRPP'):
            aux = 'do'
            
        if(res and res.group() in ['VBD', 'VBN']):
            aux = 'did'

        if(aux):
            if(type == "non_disc" or type == "Yes/No"):
                question = aux + " " + question_part + "?"

            else:
                question = type + " " + aux + " " + question_part + "?"
    if(question != ""):
        question = question[0].upper() + question[1:]
    return question

def get_named_entities(sent):
    doc = nlp(sent)
    named_entities = [(X.text, X.label_) for X in doc.ents]
    return named_entities

def get_wh_word(entity, sent):
    wh_word = ""
    if entity[1] in ['TIME', 'DATE']:
        wh_word = 'When'
        
    elif entity[1] == ['PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE']:
        wh_word = 'What'
        
    elif entity[1] in ['PERSON']:
            wh_word = 'Who'
            
    elif entity[1] in ['NORP', 'FAC' ,'ORG', 'GPE', 'LOC']:
        index = sent.find(entity[0])
        if index == 0:
            wh_word = "Who"
            
        else:
            wh_word = "Where"
            
    else:
        wh_word = "Where"
    return wh_word

def generate_one_word_questions(sent):
    
    named_entities = get_named_entities(sent)
    questions = []
    
    if not named_entities:
        return questions
    
    for entity in named_entities:
        wh_word = get_wh_word(entity, sent)
        
        if(sent[-1] == '.'):
            sent = sent[:-1]
        
        if sent.find(entity[0]) == 0:
            questions.append(sent.replace(entity[0],wh_word) + '?')
            continue
       
        question = ""
        aux_verb = False
        res = None

        for i in range(len(aux_list)):
            if(aux_list[i] in sent.split()):
                aux_verb = True
                pos = i
                break
            
        if not aux_verb:
            pos = 9
        
        text = nltk.word_tokenize(sent)
        tags = nltk.pos_tag(text)
        question_part = ""
        
        if wh_word == 'When':
            word_list = sent.split(entity[0])[0].split()
            if word_list[-1] in ['in', 'at', 'on']:
                question_part = " ".join(word_list[:-1])
            else:
                question_part = " ".join(word_list)
            
            qp_text = nltk.word_tokenize(question_part)
            qp_tags = nltk.pos_tag(qp_text)
            
            question_part = ""
            
            for i, grp in enumerate(qp_tags):
                word = grp[0]
                tag = grp[1]
                if(re.match("VB*", tag) and word not in aux_list):
                    question_part += WordNetLemmatizer().lemmatize(word,'v') + " "
                else:
                    question_part += word + " "
                
            if question_part[-1] == ' ':
                question_part = question_part[:-1]
        
        else:
            for i, grp in enumerate(tags):
                
                #Break the sentence after the first non-auxiliary verb
                word = grp[0]
                tag = grp[1]

                if(re.match("VB*", tag) and word not in aux_list):
                    question_part += word

                    if i<len(tags) and 'NN' not in tags[i+1][1] and wh_word != 'When':
                        question_part += " "+ tags[i+1][0]

                    break
                question_part += word + " "
        question = question_part.split(" "+ aux_list[pos])
        question = [aux_list[pos] + " "] + question
        question = [wh_word+ " "] + question + ["?"]
        question = ''.join(question)
        questions.append(question)
    
    return questions

def discourse():
    temp = []
    target = ""
    questions = []
    global disc_sentences
    disc_sentences = {}
    for i in range(len(sentences)):
        maxLen = 9999999
        val = -1
        for j in discourse_markers:
            tmp = len(sentences[i].split(j)[0].split(' '))  
            
            # To get valid, first discourse marker.   
            if(len(sentences[i].split(j)) > 1 and tmp >= 3 and tmp < maxLen):
                maxLen = tmp
                val = j
                
        if(val != -1):

            # To initialize a list for every new key
            if(disc_sentences.get(val, 'empty') == 'empty'):
                disc_sentences[val] = []
                
            disc_sentences[val].append(sentences[i])
            temp.append(sentences[i])


    nondisc_sentences = list(set(sentences) - set(temp))
    
    t = []
    for k, v in disc_sentences.items():
        for val in range(len(v)):
            
            # Split the sentence on discourse marker and identify the question part
            question_part = disc_sentences[k][val].split(k)[target_arg[k] - 1]
            q = generate_question(question_part, qtype[k][0])
            if(q != ""):
                questions.append([disc_sentences[k][val],q])
                
                
    for question_part in nondisc_sentences:
        s = "non_disc"
        sentence = question_part
        text = nltk.word_tokenize(question_part)
        if(text[0] == 'Yes'):
            question_part = question_part[5:]
            s = "Yes/No"
            
        elif(text[0] == 'No'):
            question_part = question_part[4:]
            s = "Yes/No"
            
        q = generate_question(question_part, s)
        if(q != ""):
            questions.append([sentence,q])
        l = generate_one_word_questions(question_part)
        questions += [[sentence,i] for i in l]
    print(len(questions))
    q={}
    for i,pair in enumerate(questions):
        q[i]=pair
        print("S: ",pair[0])
        print("Q: ",pair[1])
        print()
    return q

# sentensify()

# from nltk.corpus import stopwords

# from nltk.tokenize import word_tokenize

# sent = [' Our application proposes to create a full fledged tutorial given a text file ( Textbook chapters, pdf documents, etc) The tutorial will consist of short ppts/videos based on the text file given.',
#  '  The entire application is enabled to support various Indian regional Languages to facilitate learning in language of choice providing language agnosticism.',
#  '  In addition to this, assessments are provided after every subtopic to ensure user interaction.',
#  "  A complete user friendly web interface is created for easy use of all the features and hassle free learning and customization based on the user's preferences."]

# nltk.download('stopwords')

# stopWords = set(stopwords.words("english"))

# print (stopWords)

# sent

# from nltk.stem import WordNetLemmatizer
# from nltk.corpus import wordnet

# lemmatizer = WordNetLemmatizer()

# def nltk_tag_to_wordnet_tag(nltk_tag):
#     if nltk_tag.startswith('J'):
#         return wordnet.ADJ
#     elif nltk_tag.startswith('V'):
#         return wordnet.VERB
#     elif nltk_tag.startswith('N'):
#         return wordnet.NOUN
#     elif nltk_tag.startswith('R'):
#         return wordnet.ADV
#     else:          
#         return None

# def lemmatize_sentence(sentence):
#     #tokenize the sentence and find the POS tag for each token
#     nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))  
#     #tuple of (token, wordnet_tag)
#     wordnet_tagged = map(lambda x: (x[0], nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)
#     lemmatized_sentence = []
#     for word, tag in wordnet_tagged:
#         if tag is None:
#             #if there is no available tag, append the token as is
#             lemmatized_sentence.append(word)
#         else:        
#             #else use the tag to lemmatize the token
#             lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
#     return " ".join(lemmatized_sentence)

# nltk.download('wordnet')

# for i in range(len(sent)):
#   sent[i]=lemmatize_sentence(sent[i])

# sent

# for i in range(len(sent)):
#   sent[i]=sent[i].split()

# for i in range(len(sent)):
#   for wordi in range(len(sent[i])):
#     if sent[i][wordi] in stopWords:
#       sent[i][wordi]=""

# for i in range(len(sent)):
#   sent[i]=" ".join(sent[i])

# sent