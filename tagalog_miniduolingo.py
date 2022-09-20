import pandas as pd
import time
import random
import string

class Question:
    dividing_line= "_____________________"
    
    def correct_message(self):
        print("Correct! Good job.")
        return
    
    def incorrect_message(self):
        print("Incorrect, sorry.")
    
    def get_answer(self):
        user_answer= input("Type your answer here: ")
        user_answer= user_answer.strip().lower()
        # remove punctuation from user_answer
        user_answer= user_answer.translate(str.maketrans('', '', string.punctuation))
        return user_answer
    
    def run_sequence(self):
        self.ask()
        user_answer= self.get_answer()
        time.sleep(1)
        self.check_answer(user_answer)
        print(self.dividing_line)
        time.sleep(1)

class FillBlank(Question):
    def __init__(self, question_tl, question_en, answer):
        self.question_tl= question_tl
        self.question_en= question_en
        self.answer= answer
    
    def ask(self):
        question_tl_blank= self.question_tl.replace(self.answer, "____")
        print("Fill in the blank: \n")
        print(question_tl_blank)
        print(self.question_en + '\n')
        return
    
    def check_answer(self, user_answer):
        correct_answer= self.answer.lower()
        correct_answer= correct_answer.translate(str.maketrans('', '', string.punctuation))
        if user_answer == correct_answer:
            self.correct_message()
        else:
            self.incorrect_message()
            print("The correct answer was: {}".format(self.answer))
            
class Translate(Question):
    def __init__(self, question_tl, question_en):
        self.question_tl= question_tl
        self.question_en= question_en
        self.language= None

    def ask(self):
        language= random.choice(['tl', 'en'])
        print("Translate the following: \n")
        if language == 'tl':
            print(self.question_tl + '\n')
            self.language= 'tl'
        else:
            print(self.question_en + '\n')
            self.language= 'en'

    def check_answer(self, user_answer):
        if self.language == 'tl':
            correct_answer= self.question_en.lower()
            correct_answer= correct_answer.translate(str.maketrans('', '', string.punctuation))
            if user_answer == correct_answer:
                self.correct_message()
            else:
                self.incorrect_message()
                print("The correct answer was: {}".format(self.question_en))
        else:
            correct_answer= self.question_tl.lower()
            correct_answer= correct_answer.translate(str.maketrans('', '', string.punctuation))
            if user_answer == correct_answer:
                self.correct_message()
            else:
                self.incorrect_message()
                print("The correct answer was: {}".format(self.question_tl))
        return
    
class Lesson:
    def __init__(self, questions, completion_status=False):
        self.questions= questions
        self.completion_status= completion_status
        
    def run_lesson(self):
        for question in self.questions:
            question.run_sequence()
        self.completion_status= True
    
class FillBlankGenerator:
    def __init__(self, csv_file):
        self.csv_file= csv_file
        
    def generate_fillblank(self):
        fillblanks= []
        df= pd.read_csv(self.csv_file)
        for i in range(len(df.index)):
            question_tl= df.loc[i, "question_tl"]
            question_en= df.loc[i, "question_en"]
            answer= df.loc[i, "answer"]
            fillblanks.append(FillBlank(question_tl, question_en, answer))
        return fillblanks
    
class TranslateGenerator:
    def __init__(self, csv_file):
        self.csv_file= csv_file
    
    def generate_translate(self):
        translates= []
        df= pd.read_csv(self.csv_file)
        #for i in range(len(df.index)):
        for i in range(2):
            question_tl= df.loc[i, "question_tl"]
            question_en= df.loc[i, "question_en"]
            translates.append(Translate(question_tl, question_en))
        return translates
            
            
# TESTING FUNCTIONALITY    
# question_tl1= "Ano ang paborito mong prutas?"
# question_en1= "What is your favorite fruit?"
# answer1= "prutas"
# fillblank1= FillBlank(question_tl1, question_en1, answer1, asker1)

# questions= [fillblank1]

fillblank_generator= FillBlankGenerator('lesson1_fillblank.csv')
questions= fillblank_generator.generate_fillblank()
lesson1_fillblank= Lesson(questions)
lesson1_fillblank.run_lesson()
    
translate_generator= TranslateGenerator('lesson1_translate.csv')
questions= translate_generator.generate_translate()
lesson1_translate= Lesson(questions)
lesson1_translate.run_lesson()
