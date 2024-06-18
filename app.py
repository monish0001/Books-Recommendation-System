from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular_books.pkl','rb'))
pt = pickle.load(open('final_table.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    
    return render_template('home.html',
                        book_name = list(popular_df['Book-Title'].values),
                        author=list(popular_df['Book-Author'].values),
                        image=list(popular_df['Image-URL-M'].values),
                        votes=list(popular_df['Number-of-Rating'].values),
                        rating=list(popular_df['Average-Rating'].values)
                           )

@app.route('/about')
def about():
    return render_template('layout.html')



@app.route('/recommend')
def recommend_ui():
    return render_template('search.html')

@app.route('/recommend_books',methods=['GET','post'])
def recommend():
    user_input = request.form.get('user_input')
    data = []
    # Check if the user_input exists in the index
    if user_input not in pt.index:
        return render_template('search.html', data="Sorry, this book is not present in the database.")

    # If the book exists, find the index
    index = np.where(pt.index == user_input)[0][0]
    
    # Get the similar items
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('search.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)