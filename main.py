from flask import Flask, send_from_directory, render_template, request
import os
import sys
import db_queries


app = Flask(__name__, static_url_path='')


@app.route('/')
def main():
    if len(sys.argv) > 2:
        html_answer = render_template('header.html', name="Wiki") + db_queries.select_content("index", sys.argv[2]) + render_template('edit.html', name="index") + db_queries.select_content("index", sys.argv[2]) + render_template('footer.html')
    else:
        html_answer = render_template('header.html', name="Wiki") + db_queries.select_content("index", "") + render_template('edit.html', name="index") + db_queries.select_content("index", "") + render_template('footer.html')
    return html_answer


@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)


@app.route('/files/<path:path>')
def send_file(path):
    return send_from_directory('files', path)


@app.route('/img/')
def img_dir():
    html_answer = render_template('header.html', name="img")
    for file in os.listdir("img"):
        html_answer += f"<img src=\"/img/{file}\" width=\"20\" height=\"20\"> "
        html_answer += f"<a href=\"/img/{file}\">{file}</a><br>"
    html_answer = html_answer + render_template('edit.html', name="img") + render_template('footer.html')
    return html_answer


@app.route('/page/<path:path>')
def get_content(path):
    try:
        if len(sys.argv) > 2:
            html_answer = render_template('header.html', name=f"{path}") + db_queries.select_content(path, sys.argv[2]) + render_template('edit.html', name=f"{path}") + db_queries.select_content(path, sys.argv[2]) + render_template('footer.html')
        else:
            html_answer = render_template('header.html', name=f"{path}") + db_queries.select_content(path, "") + render_template('edit.html', name=f"{path}") + db_queries.select_content(path, "") + render_template('footer.html')
    except TypeError:
        html_answer = render_template('header.html', name=f"{path}") + "<h1>404 - not found</h1>" + render_template('edit.html', name="img") + render_template('footer.html')
    return html_answer


@app.route('/edit/', methods=['POST'])
def edit_content():
    html_content = request.form['update_html_content']
    formatted_html_content = ""
    for char in html_content:
        formatted_html_content += char
        if char == "\"":
            formatted_html_content += char

    if len(sys.argv) > 2:
        db_queries.update_content(request.form['page_name'], formatted_html_content, sys.argv[2])
    else:
        db_queries.update_content(request.form['page_name'], formatted_html_content, "")
    return f"<script>window.location = '/page/{request.form['page_name']}';</script>"


@app.route('/create_send/', methods=['POST'])
def create_content_send():
    html_content = request.form['update_html_content']
    formatted_html_content = ""
    for char in html_content:
        formatted_html_content += char
        if char == "\"":
            formatted_html_content += char
    if len(sys.argv) > 2:
        db_queries.create_content(request.form['page_name'], formatted_html_content, sys.argv[2])
    else:
        db_queries.create_content(request.form['page_name'], formatted_html_content, "")
    return f"<script>window.location = '/page/{request.form['page_name']}';</script>"


@app.route('/create/')
def create_content_template():
    return render_template('create_content.html')


@app.route('/pages/')
def get_pages():
    html_answer = render_template('header.html', name="pages")
    if len(sys.argv) > 2:
        for page in db_queries.select_pages(sys.argv[2]):
            html_answer += f"<a href=\"/page/{page[0]}\">{page[0]}</a><br>"
    else:
        for page in db_queries.select_pages(""):
            html_answer += f"<a href=\"/page/{page[0]}\">{page[0]}</a><br>"
    html_answer = html_answer + render_template('edit.html', name="img") + render_template('footer.html')
    return html_answer


@app.route('/test_editor/')
def test_editor():
    return render_template('test_editor.html')


if __name__ == "__main__":
    if len(sys.argv) > 1:
        app.run(host='0.0.0.0', port=str(sys.argv[1]))
    else:
        app.run(host='0.0.0.0')
