from flask import Flask, render_template, request

app = Flask(__name__)
@app.route('/clients', methods=['GET', 'POST'])
def clients():
	if request.method == 'GET':
		print(request.args)
		return 'hi'
	else:
		return 'bye'

def main():
	app.run(debug=True, host='grog')




if __name__ == '__main__':
	main()