from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_mysqldb import MySQL

bp = Blueprint('views', __name__)

@bp.route('/staff/')
@bp.route('/staff')
def staff():
    from app import mysql
    cursor = mysql.connection.cursor()

    position_filter = request.args.get('position')
    
    if request.method == 'GET':
        if position_filter:
            cursor.execute("SELECT * FROM staff WHERE position = %s", (position_filter,))
        else:
            cursor.execute("SELECT * FROM staff")

        staff = cursor.fetchall()
        cursor.close()
        return render_template('list.html', staff=staff)


@bp.route('/staff/json')
def staff_json():
    from app import mysql
    cursor = mysql.connection.cursor()
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM staff")
        staff = cursor.fetchall()
        cursor.close()
        return jsonify(staff)


@bp.route('/staff/create', methods=['GET', 'POST'])
def create_staff():
    from app import mysql
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form.get('name')
        position = request.form.get('pos')
        phone = request.form.get('num')
        email = request.form.get('email')
        age = request.form.get('age')
        
        cursor.execute("INSERT INTO staff (name, position, phone, email, age) VALUES (%s, %s, %s, %s, %s)", (name, position, phone, email, age))
        mysql.connection.commit()
        
        print(f"Staff member '{name}' successfully added.")
        # success_message = f"Staff member '{name}' successfully added."

        return redirect(url_for('views.staff'))
        # return render_template('create.html', success_message=success_message)
    else:
        # If the request method is GET, render the HTML form
        return render_template('create.html')

@bp.route('/staff/<int:staff_id>')
def staff_member(staff_id):
    from app import mysql
    cursor = mysql.connection.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM staff WHERE idstaff = %s", (staff_id,))
        staff = cursor.fetchone()

        ## ERROR CHECKING
        ## IF THERE IS NO STAFF MEMBER @ staff_id (STAFF MEMEBER DOES NOT EXIST)
        if staff is None:
            cursor.close()
            return render_template('member_notfound.html', staff_id=staff_id)

        cursor.close()
        return render_template('member.html', staff=staff)

@bp.route('/staff/<int:staff_id>/json')
def staff_member_json(staff_id):
    from app import mysql
    cursor = mysql.connection.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM staff WHERE idstaff = %s", (staff_id,))
        staff = cursor.fetchone()
        cursor.close()
        return jsonify(staff)
    
@bp.route('/staff/<int:staff_id>/delete', methods=['GET', 'POST'])
def staff_delete(staff_id):
    from app import mysql
    cursor = mysql.connection.cursor()
    
    if request.method == 'POST':
        cursor.execute("DELETE FROM staff WHERE idstaff = %s", (staff_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"message": f"Staff member (id: {staff_id}) was deleted successfully"})
    else:
        return render_template('delete.html', staff_id=staff_id)
    
@bp.route('/staff/<int:staff_id>/modify', methods=['GET', 'POST'])
def staff_update(staff_id):
    from app import mysql
    cursor = mysql.connection.cursor()
    
    if request.method == 'POST':
        updated_position = request.form.get('pos')
        updated_phone = request.form.get('num')
        updated_email = request.form.get('email')
        updated_age = request.form.get('age')
        
        # Execute an UPDATE query to modify the existing record
        print(f"Staff pos '{updated_position}' successfully updated.")
        print(f"Staff phone '{updated_phone}' successfully updated.")
        print(f"Staff email '{updated_email}' successfully updated.")
        print(f"Staff age '{updated_age}' successfully updated.")

        cursor.execute("UPDATE staff SET position = %s, phone = %s, email = %s, age = %s WHERE idstaff = %s", (updated_position, updated_phone, updated_email, updated_age, staff_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"message": f"Staff member (id: {staff_id}) was successfully updated!"})
    else:
        cursor.execute("SELECT name FROM staff WHERE idstaff = %s", (staff_id,))
        staff = cursor.fetchone()
        cursor.close()
        return render_template('modify.html', staff_id=staff_id, staff = staff)