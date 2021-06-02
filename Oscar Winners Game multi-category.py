from tkinter import *

import pandas as pd
import random as random
import string as string


root = Tk()
root.geometry("800x800")

#category_answer = "A"

def clickans(input):
    global category_answer
    category_answer = input

oscar_winners = pd.read_csv('.\CSV Files\oscarnominees.csv')
oscarcategories = pd.read_csv('.\CSV Files\categories.csv')
#oscaryears = pd.read_csv('.\CSV Files\Oscar_Years.csv')
randomyearquestion = pd.read_csv('.\CSV Files\RandomYear.csv')
question_letters = pd.read_csv('.\CSV Files\QuestionLetters.csv')
number_of_categories = len(oscarcategories)

# Any variables that aren't going to change throughout the program are defined at the top of the script
#region Constant_Variables
number_of_questions = 10

csv_header_year = "YEAR"
csv_header_category = "CATEGORY"
csv_header_name = "NAME"
csv_header_is_winner = "WINORLOSE"

quiz_category_name = 'Actor in a leading role'

category_selection_option = "Option"
category_selection_description = "Category"

all_categories_by_year = oscar_winners.drop_duplicates([csv_header_year,csv_header_category]) #finds all years and categories to enable a quiz to only randomise where category was awarded in in years
all_categories = oscar_winners.drop_duplicates([csv_header_category])[csv_header_category]

category_index = 0
category_letters = list(string.ascii_uppercase)

cat_answers_matrix_headers = [category_selection_option, category_selection_description]
#cat_answers_matrix_data = [[0, 0]]
cat_answers_dataframe = pd.DataFrame(columns=cat_answers_matrix_headers)

# Generate list of categories for
for j, row in oscarcategories.iterrows():
    letter = category_letters[category_index]
    category_text = (row[csv_header_category])
    cat_answers_dataframe = cat_answers_dataframe.append({category_selection_option: letter, category_selection_description: category_text} , ignore_index=True)

    category_index += 1

cat_answers_dataframe = cat_answers_dataframe.append({category_selection_option: "X", category_selection_description: "Random Category"} , ignore_index=True)
cat_answers_dataframe = cat_answers_dataframe.append({category_selection_option: "Y", category_selection_description: "Fully Random"} , ignore_index=True)

#print("category answer matrix hack")
temp_length_categories = len(cat_answers_dataframe)
print(cat_answers_dataframe.to_string(index=False))

##############################
##############################

topFrame = Frame(root)

topFrame = Label(root, text="Please select a category")
topFrame.pack()
button_frame = Frame(root)
button_frame = Label(root, text=temp_length_categories)
button_frame.pack(side=BOTTOM)
#print(temp_length_categories)
for b, row in cat_answers_dataframe.iterrows():

    #category_selection_option
    #print(cat_answers_dataframe[category_selection_description].iloc[b])
    button_text = cat_answers_dataframe[category_selection_option].iloc[b]
    button_label = cat_answers_dataframe[category_selection_description].iloc[b]

    button_x = Button(button_frame, text=button_text, command=lambda button_text=button_text: clickans(button_text), width=5)
    button_x.grid(row=b, column=0)

    button_x = Label(button_frame, text=button_label)
    button_x.grid(row=b, column=1)



root.mainloop()



#############################


# category_answer = input("Please pick your category selection :").upper()


if category_answer == "X":
    chosen_category = oscarcategories.iloc[random.randint(0, number_of_categories)][csv_header_category]
    print (chosen_category)
elif category_answer == "Y":
    ############### NEEDS WORK
    chosen_category = 'ACTOR IN A LEADING ROLE'
else:
    chosen_category = cat_answers_dataframe[(cat_answers_dataframe[category_selection_option]==category_answer)][category_selection_description].iloc[0]



print ('You have chosen: ', chosen_category)
#category_answer

question_years = list(all_categories_by_year[all_categories_by_year[csv_header_category] == chosen_category][csv_header_year])




random.shuffle(question_years)
question_letters = list(string.ascii_uppercase)

correct_answers = 0
for i, question_year in enumerate(question_years):
    question_number = i + 1
    oscar_nominees_for_year = oscar_winners.loc[oscar_winners[csv_header_year] == question_year]
    category_nominees_for_year = oscar_nominees_for_year.loc[oscar_nominees_for_year[csv_header_category] == chosen_category]

    print('To quit at any time, type "QUIT" in the answer field.\n\n')
    print('Question', question_number, 'Who won the Oscar for', chosen_category, 'in', question_year, '?\n')

    winning_letter = None
    winning_text = None
    question_index = 0



    for j, row in category_nominees_for_year.iterrows():
        letter = question_letters[question_index]
        nominee = row[csv_header_name]

        if row[csv_header_is_winner]:
            winning_letter = letter
            winning_text = nominee

        print("{0}. {1}".format(letter, nominee))
        question_index += 1

    answer = input("Please enter your answer :").upper()

    if answer == winning_letter:
        print('Well done! That is correct!\n')
        correct_answers += 1
    elif answer == 'QUIT':
        break
    else:
        print('Sorry, wrong answer! The correct answer was:', winning_letter, ':', winning_text, '\n')

    final_score_percentage = ('{0}%'.format(int(100 * correct_answers / len(question_years))))
    print('You have answered', correct_answers, '(', final_score_percentage, ')', 'correctly out of', len(question_years), 'questions.')

print('That is the end of the quiz.')




