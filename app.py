from flask import Flask,render_template,request,redirect,url_for,jsonify,send_from_directory
import os
from models import DBManager
from flask import  flash,session
import math

# from datetime import datetime


app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = 'static/uploads'

app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

manager = DBManager()
@app.route('/')
def index():

    return render_template('index.html')
#### 포스트 관련###
# 목록보기
@app.route('/post') 
def post():
    # 페이지당 표시할 게시글 수
    per_page = 5

    # 현재 페이지 번호 (기본값: 1)
    page = request.args.get('page', 1, type=int)

    # 해당 페이지에 해당하는 게시글들 가져오기
    posts = manager.get_all_posts(page, per_page)

    # 전체 게시글 수 가져오기
    total_count = manager.get_total_post_count()

    # 총 페이지 수 계산
    total_pages = math.ceil(total_count / per_page)
    return render_template('post.html',posts=posts, total_pages=total_pages, current_page=page)

# 내용추가
# 파일업로드: enctype="multipart/form-data", method='POST', type='file', accept=".png,.jpg,.gif" 
@app.route('/post/add', methods=['GET', 'POST']) ## 게시글 추가
def add_post():
    if 'userid' not in session:
        return redirect(url_for('login'))  # 로그인 페이지 경로를 'login'으로 설정한다고 가정
    
    userid = session['userid']  # 로그인한 사용자 ID 가져오기
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        # 첨부파일 한 개
        file = request.files['file']
        filename = file.filename if file else None
        
        if filename:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
        
        if manager.insert_post(title,content,filename,userid):
            return redirect(url_for('post'))
        return "게시글 추가 실패", 400        
    return render_template('add.html')

# 내용보기# 내용보기
@app.route('/post/<int:id>')   # 내용 보기 ### (comments)
def view_post(id):
    
    post = manager.get_post_by_id(id) #내용 보기 (디테일 보는거)
    
    manager.counting_view(id)
    
    comments=manager.comment_view(id)
    return render_template('view.html',post=post,comments=comments)

@app.route('/post/edit/<int:id>', methods=['GET', 'POST']) ## 게시글 수정
def edit_post(id):
    ##check id를 위해 userid를 변수로 저장
    userid= session['userid']

    if 'userid' not in session:
        
        flash("로그인을 하세요.")
        return redirect(url_for('login'))  # 로그인 페이지 경로를 'login'으로 설정한다고 가정
    ## checkid라는걸 하기위해 post_man이라는 변수에 값을 저장
    post_man = manager.check_id(id)## 여기서 반환하는값은 fetchone 으로 받게되어,dictionary=true의 세팅으로 받게된 반환값은 dictionary 구조 임

    if post_man['userid'] != userid: ## 딕셔너리 구조라서 항상 다르게 출력되었어서, post_man 변수뒤에['userid']를 달아줌( 이렇게되면 밸류값만 출력 )
        flash("이시끼야 니가만든거아니잖아")
        return redirect(url_for('view_post',id=id))    ## 수정,삭제에 실패하게되면, view_post 함수에 들렀다 오기때문에 view함수에 있는 조회수에 들렀다와서 뷰수가 늘어나고있음.
    
    post = manager.get_post_by_id(id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        file = request.files['file']
        filename = file.filename if file else None
        
        if filename:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        if manager.update_post(id,title,content,filename):
            return redirect("/")
        return "게시글 추가 실패", 400        
    return render_template('edit.html',post=post) 

@app.route('/post/delete/<int:id>')  #게시글 삭제
def deleting_post(id):
    userid= session['userid']
    if 'userid' not in session:
        
        flash("로그인을 하세요.")### 일단 로그인을 해야 삭제가 되게끔 까지만 처리상태, 나중에 동일한 userid 일때만 처리되게끔 작업해야.
        return redirect(url_for('login'))  # 로그인 페이지 경로를 'login'으로 설정한다고 가정

    post_man = manager.check_id(id)

    if post_man['userid'] != userid: ## 딕셔너리 구조라서 항상 다르게 출력됬었음..
        flash("이시끼야 니가만든거아니잖아")
        return redirect(url_for('view_post',id=id))
    
    if manager.delete_post(id):
        return redirect(url_for('view_post',id=id))
    return "게시글 삭제 실패", 400








##################로그인 ##################

@app.route('/register',methods=['GET','POST'])  ## 레지스터(아이디 등록)
def register():
    if request.method=='POST':
        username=request.form['username']
        userid=request.form['userid']
        password=request.form['password']
        confirm_password=request.form['confirm_password']
        if password != confirm_password:
            flash("비밀번호가 일치하지 않습니다.")
            return redirect(url_for('register'))
        
        if manager.check_user_exists(userid):
            flash("이미 사용 중인 아이디입니다.")
            return redirect(url_for('register'))
        # return username
        # return username
        if manager.regist_account(username, userid, password):
            flash("회원가입이 완료되었습니다.")
            return redirect('/login')
        else:
            flash("계정 등록 실패. 다시 시도해주세요.")
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST']) ## 로그인
def login():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        
        # 아이디와 비밀번호 확인
        if manager.verify_user(userid, password):
            
            session['userid'] = userid  # 세션에 사용자 정보 저장
            flash("로그인 성공!")
            return redirect(url_for('index'))  # 로그인 성공 후 대시보드로 리디렉션
        
        flash("아이디나 비밀번호가 틀렸습니다.")  # 로그인 실패 메시지
        return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/logout') ## 로그아웃 
def logout():
    
    session.pop('userid', None)  # 세션
    
    flash("로그아웃되었습니다.")
    return redirect(url_for('login'))

### post와 비슷한 형식의 소스, event로 이름만 바꿈
@app.route('/events') 
def event():
    # 페이지당 표시할 게시글 수
    per_page = 5

    # 현재 페이지 번호 (기본값: 1)
    page = request.args.get('page', 1, type=int)

    # 해당 페이지에 해당하는 게시글들 가져오기
    events = manager.get_all_events(page, per_page)

    # 전체 게시글 수 가져오기
    total_count = manager.get_total_post_count()

    # 총 페이지 수 계산
    total_pages = math.ceil(total_count / per_page)
    return render_template('event_post.html',events=events, total_pages=total_pages, current_page=page)

# 내용추가
# 파일업로드: enctype="multipart/form-data", method='POST', type='file', accept=".png,.jpg,.gif" 
@app.route('/event/add', methods=['GET', 'POST']) ## 게시글 추가
def add_event():
    if 'userid' not in session:
        return redirect(url_for('login'))  # 로그인 페이지 경로를 'login'으로 설정한다고 가정
    
    userid = session['userid']  # 로그인한 사용자 ID 가져오기
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        location = request.form['location']
        category = request.form['category']
        
        # 첨부파일 한 개
        file = request.files['file']
        filename = file.filename if file else None
        
        if filename:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
        
        if manager.insert_event(title, description, start_date, end_date, location, category, filename, userid):
            return redirect("/")
        return "게시글 추가 실패", 400        
    return render_template('event_add.html' )

# 내용보기# 내용보기
@app.route('/event/<int:id>')   # 내용 보기 ( 하나만 보는거 )
def view_event(id):
    
    event = manager.get_event_by_id(id) #내용 보기 (디테일 보는거)
    manager.counting_event_view(id)
    return render_template('event_view.html',event=event)
## db 만들고 넣어야함
@app.route('/event/edit/<int:id>', methods=['GET', 'POST']) ## 게시글 수정
def edit_event(id):
    
    if 'userid' not in session:
        
        flash("로그인을 하세요.")
        return redirect(url_for('login'))  # 로그인 페이지 경로를 'login'으로 설정한다고 가정
    
    event = manager.get_event_by_id(id)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        location = request.form['location']
        category = request.form['category']
        
        file = request.files['file']
        filename = file.filename if file else None
        
        if filename:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if manager.update_event(title, description, start_date, end_date, location, category, filename,id):
            
            return redirect("/")
        return "게시글 추가 실패", 400        
    return render_template('event_edit.html',event=event)

@app.route('/event/delete/<int:id>')  #게시글 삭제
def deleting_event(id):
    if 'userid' not in session:
        
        flash("로그인을 하세요.")### 일단 로그인을 해야 삭제가 되게끔 까지만 처리상태, 나중에 동일한 userid 일때만 처리되게끔 작업해야.
        return redirect(url_for('login'))  # 로그인 페이지 경로를 'login'으로 설정한다고 가정
    
    
    if 'userid' not in session:
        return redirect(url_for('login'))  # 로그인 페이지 경로를 'login'으로 설정한다고 가정
    
    if manager.delete_event(id):
        return redirect(url_for('index'))
    return "게시글 삭제 실패", 400

@app.route('/comment/add/<int:post_id>', methods=['GET', 'POST']) ## 게시글 추가
def add_comment(post_id):
    if 'userid' not in session:
        return redirect(url_for('login'))  # 로그인 페이지 경로를 'login'으로 설정한다고 가정
    
    userid = session['userid']  # 로그인한 사용자 ID 가져오기
    
    if request.method == 'POST':
        comment = request.form['comment']

        if manager.insert_comment(comment, userid, post_id): ## (comment, userid, post_id 넘겨주는값에 post_id도 포함이되어야 내가원하는 게시글에 댓글생성)
 ### 리다이렉트 url_for로 다른 렌더링 함수를 넣게되면 그리로 들어가게되는데, 대상 동적변수, 함수내에서 지정받은 변수를 입력하게되면 된다.
            return redirect(url_for('view_post',id=post_id))
        return "게시글 추가 실패", 400        
    return render_template('view.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5007,debug=True)