from tooltron import *
from flask import Flask, render_template, request

app = Flask(__name__)
@app.route('/clients', methods=['GET', 'POST'])

def process_get_request(request):
	idNum = request.args.get('ID')
	return machine_clearance(idNum)

def clients():
	if request.method == 'GET':
		return process_get_request(request)
	else:
		return 'bye'

def main():
	app.run(debug=True, port='3996')




if __name__ == '__main__':
	main()