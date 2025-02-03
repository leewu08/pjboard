import mysql.connector
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy



class DBManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="10.0.66.8",
                user="sejong",
                password="1234",
                database="board_db3"
            )
            self.cursor = self.connection.cursor(dictionary=True)
            
        except mysql.connector.Error as error:
            print(f"데이터베이스 연결 실패: {error}")

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            
####post 

## post 를 페이지네이션해서 보기위하여 두개로 쪼갰다            
            
    # def get_all_posts(self,page=1,posts_per_page=10): ## 작성되어있는 포스트들 다 보기
    #     try:
    #         self.connect()
    #         ##(요고는 페이지네이션 기능 추가전 sql문)
    #         # sql = "SELECT * FROM posts" # select *from posts < 포스트에있는 모든 요소들을 보게 되어있음.
    #         # self.cursor.execute(sql)
    #         # 
            
    #         # 페이지 번호와 페이지당 게시물 수에 따라 OFFSET 계산
    #         offset = (page - 1) * posts_per_page
            
    #         # SQL 쿼리에서 LIMIT와 OFFSET 사용
    #         sql = f"SELECT * FROM posts LIMIT {posts_per_page} OFFSET {offset}"
    #         self.cursor.execute(sql)
    #         return self.cursor.fetchall() # 그 요소중 펫치 올, 하게되어 모든요소들을 보게됨
            
    #     except mysql.connector.Error as error: 
    #         print(f"게시글 조회 실패: {error}")
    #         return []
    #     finally:
    #         self.disconnect()
            
    def get_all_posts(self, page, per_page):
        try:
            self.connect()
            offset = (page - 1) * per_page  # OFFSET을 계산
            sql = 'SELECT * FROM posts ORDER BY created_at DESC LIMIT %s OFFSET %s'##(order by를 넣음으로서, 최신에 작성한 문서가 제일위로오게)
            self.cursor.execute(sql, (per_page, offset))
            return self.cursor.fetchall()  # 지정된 페이지에 해당하는 게시글들 반환
        except mysql.connector.Error as error:
            print(f'게시글 조회 실패 : {error}')
            return []
        finally:
            self.disconnect()        
                     
    def get_total_post_count(self):
        try:
            self.connect()
            sql = 'SELECT COUNT(*) AS total_count FROM posts'
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            return result['total_count']  # 총 게시글 수 반환
        except mysql.connector.Error as error:
            print(f'게시글 수 조회 실패 : {error}')
            return 0
        finally:
            self.disconnect()  




    
    def insert_post(self,title,content,filename,userid):
        try:
            self.connect()
            sql = "INSERT INTO posts (title,content,filename,created_at,userid) values (%s,%s,%s,%s,%s)"
            values = (title,content,filename,datetime.now(),userid)            
            self.cursor.execute(sql, values)
            
            #values = [(name,email,department,salary,datetime.now().date()),(name,email,department,salary,datetime.now().date())]
            #self.cursor.executemany(sql, values)            
            
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            self.connection.rollback()
            print(f"내용 추가 실패: {error}")
            return False
        finally:
            self.disconnect()
            
    def counting_view(self,id):
        try:
            self.connect()
            sql = "update posts set views = views+1 WHERE id = %s"
            value = (id,) # 튜플 1개 일때
            self.cursor.execute(sql, value)
            self.connection.commit()  # 변경사항을 DB에 반영
            
            
            # 게시글 정보 조회
            sql_select = "SELECT * FROM posts WHERE id = %s"
            self.cursor.execute(sql_select, value)
            post = self.cursor.fetchone()  # 게시글 정보 가져오기

            
            if post:
                return post
            else:
                return None  # 게시글이 없으면 None 반환
        except mysql.connector.Error as error:
            print(f"내용 조회 실패: {error}")
            return None
        finally:
            self.disconnect()
            
    # def like_it(self,id):
    #     try:
    #         self.connect()
    #         sql = "update posts set likes = likes+1 WHERE id = %s"
    #         value = (id,) # 튜플 1개 일때
    #         self.cursor.execute(sql, value)
    #         self.connection.commit()  # 변경사항을 DB에 반영
            
            
    #         # 게시글 정보 조회
    #         sql_select = "SELECT * FROM posts WHERE id = %s"
    #         self.cursor.execute(sql_select, value)
    #         post = self.cursor.fetchone()  # 게시글 정보 가져오기

    #         if post:
    #             return post
    #         else:
    #             return None  # 게시글이 없으면 None 반환
    #     except mysql.connector.Error as error:
    #         print(f"내용 조회 실패: {error}")
    #         return None
    #     finally:
    #         self.disconnect()
   
    def get_post_by_id(self, id):
        try:
            self.connect()
            sql = "SELECT * FROM posts WHERE id = %s"
            value = (id,) # 튜플 1개 일때
            self.cursor.execute(sql, value)
            return self.cursor.fetchone() # 하나의 결과만 필요할때 사용하는 메서드(첫번째행만 가져오게됨, 결과가 없으면 none 반환)
        except mysql.connector.Error as error:
            print(f"내용 조회 실패: {error}")
            return None
        finally:
            self.disconnect()
    
    def update_post(self,id,title,content,filename):
        try:
            self.connect()
            if filename:
                sql = """UPDATE posts 
                        SET title = %s, content = %s, filename = %s 
                        WHERE id = %s
                        """
                values = (title,content,filename,id)
            else:
                sql = """UPDATE posts 
                        SET title = %s, content = %s 
                        WHERE id = %s
                        """
                values = (title,content,id)
            self.cursor.execute(sql, values)
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            self.connection.rollback()
            print(f"게시글 수정 실패: {error}")
            return False
        finally:
            self.disconnect()
    
    def delete_post(self, id):
        
        try:
            self.connect()
            sql = "DELETE FROM posts WHERE id = %s"
            value = (id,) # 튜플 1개 일때
            self.cursor.execute(sql, value)
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            self.connection.rollback()
            print(f"게시판 삭제 실패: {error}")
            return False
        finally:
            self.disconnect()



###        기능 로그인      ####

#### 2개의함수가 register():에 묶여있음 ####-----------------

            
            
    def check_user_exists(self, userid):
        
        try:
            
            self.connect()
            sql = 'SELECT * FROM data WHERE userid = %s'
            self.cursor.execute(sql, (userid,))
            result = self.cursor.fetchone()  # 중복된 아이디가 있으면 반환됨
            if result:
                return True
            else:
                return False
        except mysql.connector.Error as error:
            print(f'아이디 중복 체크 실패: {error}')
            return False
        finally:
            self.disconnect()
            ## 위 함수가 충족되면
            
    def regist_account(self,username,userid,password): 
        try:
            self.connect()       
            # if self.check_user_exists(userid):
            #     return False

            sql='insert into data(username,userid,password) values (%s,%s,%s)'
            values=(username,userid,password)
            self.cursor.execute(sql,values)
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            print(f'account 추가실패 : {error}') 
            return False
        finally:
            self.disconnect()
            ## 아래함수 실행
            
####--------------------------------------------------

            

    def verify_user(self, userid, password):
        """사용자가 입력한 아이디와 비밀번호를 확인"""
        try:
            self.connect()
            sql = 'SELECT username, password FROM data WHERE  userid = %s'
            self.cursor.execute(sql, (userid,))
            result = self.cursor.fetchone()
            
            if result:
                stored_password = result['password']  # 데이터베이스에서 가져온 해시된 비밀번호
                #if check_password_hash(stored_password, password):
                    # 해시된 비밀번호와 비교
                if stored_password == password:
                    return result['username']  # 비밀번호 일치
            return False  # 아이디 없음 또는 비밀번호 불일치
        except mysql.connector.Error as error:
            print(f'비밀번호 확인 실패: {error}')
            return False
        finally:
            self.disconnect()
            
# #### 기능 이벤트###

    def get_all_events(self, page, per_page):
        try:
            self.connect()
            offset = (page - 1) * per_page  # OFFSET을 계산
            sql = 'SELECT * FROM events ORDER BY created_at DESC LIMIT %s OFFSET %s' ##(order by를 넣음으로서, 최신에 작성한 문서가 제일위로오게)
            self.cursor.execute(sql, (per_page, offset))
            return self.cursor.fetchall()  # 지정된 페이지에 해당하는 게시글들 반환
        except mysql.connector.Error as error:
            print(f'게시글 조회 실패 : {error}')
            return []
        finally:
            self.disconnect()        
                     
    def get_total_event_count(self):
        try:
            self.connect()
            sql = 'SELECT COUNT(*) AS total_count FROM events'
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            return result['total_count']  # 총 게시글 수 반환
        except mysql.connector.Error as error:
            print(f'게시글 수 조회 실패 : {error}')
            return 0
        finally:
            self.disconnect()  




    
    def insert_event(self, title, description, start_date, end_date, location, category, filename, userid):
        try:
            self.connect()
            sql = """
            INSERT INTO events (title, description, start_date, end_date, location, category, filename, userid, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (title, description, start_date, end_date, location, category, filename, userid, datetime.now())            
            self.cursor.execute(sql, values)   
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            self.connection.rollback()
            print(f"내용 추가 실패: {error}")
            return False
        finally:
            self.disconnect()
            
    def counting_event_view(self,id):
        try:
            self.connect()
            sql = "update events set views = views+1 WHERE id = %s"
            value = (id,) # 튜플 1개 일때
            self.cursor.execute(sql, value)
            self.connection.commit()  # 변경사항을 DB에 반영
            
            
            # 게시글 정보 조회
            sql_select = "SELECT * FROM events WHERE id = %s"
            self.cursor.execute(sql_select, value)
            event = self.cursor.fetchone()  # 게시글 정보 가져오기

            
            if event:
                return event
            else:
                return None  # 게시글이 없으면 None 반환
            
            
        except mysql.connector.Error as error:
            print(f"내용 조회 실패: {error}")
            return None
        finally:
            self.disconnect()
 

    def get_event_by_id(self, id):
        try:
            self.connect()
            sql = "SELECT * FROM events WHERE id = %s"
            value = (id,) # 튜플 1개 일때
            self.cursor.execute(sql, value)
            return self.cursor.fetchone() # 하나의 결과만 필요할때 사용하는 메서드(첫번째행만 가져오게됨, 결과가 없으면 none 반환)
        except mysql.connector.Error as error:
            print(f"내용 조회 실패: {error}")
            return None
        finally:
            self.disconnect()
    
    def update_event(self,title, description, start_date, end_date, location, category, filename,id):
        try:
            self.connect()
            if filename:
                sql = """UPDATE events 
                        SET title = %s, description = %s, start_date = %s ,end_date=%s,
                        location =%s, category=%s,filename=%s
                        WHERE id = %s
                        """
                        
                values = (title, description, start_date, end_date, location, category, filename,id)
            else:
                sql = """UPDATE events 
                        SET title = %s, description = %s, start_date = %s ,end_date=%s,
                        location =%s, category=%s
                        WHERE id = %s
                        """
                values = (title, description, start_date, end_date, location, category,id)
            self.cursor.execute(sql, values)
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            self.connection.rollback()
            print(f"게시글 수정 실패: {error}")
            return False
        finally:
            self.disconnect()
    
    def delete_event(self, id):
        try:
            self.connect()
            sql = "DELETE FROM events WHERE id = %s"
            value = (id,) # 튜플 1개 일때
            self.cursor.execute(sql, value)
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            self.connection.rollback()
            print(f"게시판 삭제 실패: {error}")
            return False
        finally:
            self.disconnect()



# 댓글기능

    def insert_comment(self, content, userid, post_id):
        try:
            self.connect()
            sql = """
            INSERT INTO comments (content, userid, post_id ,created_at)
            VALUES (%s, %s, %s,%s)
            """
            values = (content,userid,post_id,datetime.now())            
            self.cursor.execute(sql, values)   
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            self.connection.rollback()
            print(f"내용 추가 실패: {error}")
            return False
        finally:
            self.disconnect()
            
    def comment_view(self,id):
        try:
            self.connect()
            sql = 'SELECT * FROM comments WHERE post_id =%s' 
            self.cursor.execute(sql,(id,))
            return self.cursor.fetchall()  # 지정된 페이지에 해당하는 게시글들 반환
        except mysql.connector.Error as error:
            print(f'게시글 조회 실패 : {error}')
            return []
        finally:
            self.disconnect()        
            
    def check_id(self,id):
        try:
            self.connect()
            sql = 'SELECT userid FROM posts WHERE id =%s' 
            self.cursor.execute(sql,(id,))
            poster=self.cursor.fetchone() # 지정된 페이지에 해당하는 게시글들 반환
            return poster 
        except mysql.connector.Error as error:
            print(f'게시글 조회 실패 : {error}')
            return []
        finally:
            self.disconnect()        