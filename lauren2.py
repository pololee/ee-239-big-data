from tuan5 import process_line 
##########Question 6##########

###answers.csv parser###
def question_6a(file_name, line_number):
	answers_file = open(file_name,  mode='r')
	
	num_lines = 0
	chosen_line = ""
	
	for line in answers_file:
		num_lines += 1
		if num_lines == line_number:
			chosen_line = line
			
	answers_file.close()
	
	if chosen_line == "": #invalid line number
		print("Line number out of range!")
		exit(1)

	return process_line(chosen_line)

###users.csv parser###
def question_6b(file_name, line_number):
	
	users_file = open(file_name,  mode='r')
	
	num_lines = 0
	chosen_line = ""
	
	for line in users_file:
		num_lines += 1
		if num_lines == line_number:
			chosen_line = line
			
	users_file.close()
	
	if chosen_line == "": #invalid line number
		print("Line number out of range!")
		exit(1)

	return process_line(chosen_line)
	
if __name__ == "__main__":
	list = question_6a("answers.csv", 2)
	print list