import difflib
from difflib import SequenceMatcher
import Levenshtein
import csv

def similarity_check(cleaned_answer,cleaned_input):
    distance = Levenshtein.distance(cleaned_answer, cleaned_input)
    max_len = max(len(cleaned_answer), len(cleaned_input))
    similarity_ratio = 1 - (distance / max_len)

    return similarity_ratio

def word_error_rate(ground_truth, recognized_text):
    return Levenshtein.distance(ground_truth, recognized_text) / len(ground_truth.split())

def character_error_rate(ground_truth, recognized_text):
    return Levenshtein.distance(ground_truth, recognized_text) / len(ground_truth)

def precision_recall_f1(ground_truth, recognized_text):
    true_positives = sum([1 for token in recognized_text.split() if token in ground_truth])
    false_positives = max(len(recognized_text.split()) - true_positives, 0)
    false_negatives = max(len(ground_truth.split()) - true_positives, 0)

    precision = true_positives / (true_positives + false_positives) if true_positives + false_positives > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if true_positives + false_negatives > 0 else 0

    f1_score = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
    
    return precision, recall, f1_score

def levenshtein_distance(ground_truth, recognized_text):
    return Levenshtein.distance(ground_truth, recognized_text)

def testing_without(output_csv_path,path_answer,path_input):
    # Open the CSV file in write mode
    with open(output_csv_path, 'w', newline='') as csvfile:
        # Create a CSV writer object
        csvwriter = csv.writer(csvfile)

        # Write the header row
        csvwriter.writerow(['Image', 'Word Error Rate', 'Character Error Rate', 'Precision', 'Recall', 'F1 Score', 'Levenshtein Distance', 'Similarity Ratio'])

        for i in range(1,11):
            # Read answer file
            file_path_answer = path_answer+f'{i}.txt'
            with open(file_path_answer, 'r') as file:
                answer = file.read()
            
            # Remove spaces, tabs, and Enter
            cleaned_answer = answer.replace(" ", "").replace("\t", "").replace("\n", "")

            # Read input file
            file_path_input = path_input+f'{i}.txt'
            with open(file_path_input, 'r') as file:
                input = file.read()

            # Remove spaces, tabs, and Enter
            cleaned_input = input.replace(" ", "").replace("\t", "").replace("\n", "")

            wer_score = word_error_rate(cleaned_answer, cleaned_input)
            cer_score = character_error_rate(cleaned_answer, cleaned_input)
            precision, recall, f1_score = precision_recall_f1(cleaned_answer, cleaned_input)
            levenshtein_dist = levenshtein_distance(cleaned_answer, cleaned_input)
            

            print(f"Image {i}")
            print(f"Word Error Rate: {wer_score}")
            print(f"Character Error Rate: {cer_score}")
            print(f"Precision: {precision}, Recall: {recall}, F1 Score: {f1_score}")
            print(f"Levenshtein Distance: {levenshtein_dist}")
            print(f"Similarity Ratio without SPACE/TAB/ENTER = {similarity_check(cleaned_answer,cleaned_input)*100}")
            
            # Write the results to the CSV file
            csvwriter.writerow([f"Image {i}", wer_score, cer_score, precision, recall, f1_score, levenshtein_dist, similarity_check(answer, input)*100])

                        
def testing_with(output_csv_path,path_answer,path_input):
    # Open the CSV file in write mode
    with open(output_csv_path, 'w', newline='') as csvfile:
        # Create a CSV writer object
        csvwriter = csv.writer(csvfile)

        # Write the header row
        csvwriter.writerow(['Image', 'Word Error Rate', 'Character Error Rate', 'Precision', 'Recall', 'F1 Score', 'Levenshtein Distance', 'Similarity Ratio'])

        for i in range(1,11):
            # Read answer file
            file_path_answer = path_answer+f'{i}.txt'
            with open(file_path_answer, 'r') as file:
                answer = file.read()

            # Read input file
            file_path_input = path_input+f'{i}.txt'
            with open(file_path_input, 'r') as file:
                input = file.read()

            cleaned_answer = answer
            cleaned_input = input    
            wer_score = word_error_rate(cleaned_answer, cleaned_input)
            cer_score = character_error_rate(cleaned_answer, cleaned_input)
            precision, recall, f1_score = precision_recall_f1(cleaned_answer, cleaned_input)
            levenshtein_dist = levenshtein_distance(cleaned_answer, cleaned_input)
            

            print(f"Image {i}")
            print(f"Word Error Rate: {wer_score}")
            print(f"Character Error Rate: {cer_score}")
            print(f"Precision: {precision}, Recall: {recall}, F1 Score: {f1_score}")
            print(f"Levenshtein Distance: {levenshtein_dist}")
            print(f"Similarity Ratio without SPACE/TAB/ENTER = {similarity_check(cleaned_answer,cleaned_input)*100}")
            
            # Write the results to the CSV file
            csvwriter.writerow([f"Image {i}", wer_score, cer_score, precision, recall, f1_score, levenshtein_dist, similarity_check(answer, input)*100])

testing_without('./result_without.csv','./answer/','./input/')
testing_with('./result_with.csv','./answer/','./input/')
testing_without('./baseline_without.csv','./answer/','./baseline/')
testing_with('./baseline_with.csv','./answer/','./baseline/')