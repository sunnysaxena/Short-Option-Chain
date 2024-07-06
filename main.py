from website import create_app

app = create_app()

if __name__ == '__main__':
    print('start...')
    # app.run(debug=True, port=8000)
    app.run(debug=True)
    # app.run(debug=True, host="0.0.0.0", port=8000)
