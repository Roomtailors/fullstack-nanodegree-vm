from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from restaurants import Base, Restaurant
import cgi

engine = create_engine('sqlite:///restaurants.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

    def success_header(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # Read form data
    def set_form_data(self):
        ctype, pdict = cgi.parse_header(
            self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            return cgi.parse_multipart(self.rfile, pdict)
        return

    def get_record_by_url(self):
        recordID = self.path.split('/')[-2]
        record = session.query(Restaurant).filter_by(id=recordID).first()
        return record

    def write_output(self, output):
        output = "<html><body>" + output + "</body></html>"
        self.wfile.write(output)
        print output

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.success_header()

                restaurants = session.query(Restaurant).order_by(Restaurant.name.asc()).all()
                output = ""
                output += "<h1>List of restaurants</h1>"
                for entry in restaurants:
                    output += "<p>"
                    output += entry.name
                    output += " <a href='/restaurants/" + str(entry.id) + "/edit'>Edit</a> | <a href='/restaurants/" + str(entry.id) + "/delete'>Delete</a>"
                    output += "</p>"

                output += "<a href='/restaurants/new'>New restaurant</a>"
                self.write_output(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.success_header()
                output = ""
                output += "<h1>Create new restaurant</h1>"
                output += "<form method='post' enctype='multipart/form-data'>"
                output += "<input name='name' type='text' placholder='Restaurant name'>"
                output += "<input type='submit' value='Create new entry'>"
                output += "</form>"
                self.write_output(output)
                return

            if self.path.endswith("/delete"):
                self.success_header()
                recordID = self.path.split('/')[-2]
                output = ""
                output += "<h1>Delete restaurant</h1>"
                output += "<p>Holy moly! Are you sure you want to delete restaurant #" + str(recordID) + "?!?!"
                output += "<form method='post' enctype='multipart/form-data'>"
                output += "<input type='submit' value='Delete'>"
                output += "</form>"
                output += "<a href='/restaurants'>Sissy-out</a>"
                self.write_output(output)
                return

            if self.path.endswith("/edit"):
                self.success_header()
                restaurantRecord = self.get_record_by_url()

                if restaurantRecord:
                    output = ""
                    output += "<h2>Edit record" + restaurantRecord.name + "</h2>"
                    output += "<form method='post' enctype='multipart/form-data'>"
                    output += "<input name='name' type='text' placholder='Restaurant name' value='" + restaurantRecord.name + "'>"
                    output += "<input type='submit' value='Create new entry'>"
                    output += "</form>"
                    self.write_output(output)

                else:
                    output = ""
                    output += "<h2>Record not found</h2>"
                    self.write_output(output)

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                fields = self.set_form_data()
                restaurant_name = fields.get('name')

                newEntry = Restaurant(name=restaurant_name[0])
                session.add(newEntry)
                session.commit()

                output = ""
                output += " <h2> Your new restaurant: </h2>"
                output += "<h1> %s </h1>" % restaurant_name[0]
                output += "<br/><a href='/restaurants'>Back to list</a>"
                self.write_output(output)
                return

            if self.path.endswith("/delete"):
                deleteRecord = self.get_record_by_url()

                if deleteRecord:
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    session.delete(deleteRecord)
                    session.commit()

                    output = ""
                    output += "<h2>The restaurant " + str(deleteRecord.name) + " has been deleted</h2>"
                    output += "<a href='/restaurants'>Back to the bunch</a>"
                    self.write_output(output)
                    return

                else:
                    self.send_response(301)
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/edit"):
                restaurantRecord = self.get_record_by_url()

                if restaurantRecord:
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    fields = self.set_form_data()
                    restaurant_name = fields.get('name')
                    restaurantRecord.name = restaurant_name[0]
                    session.commit()

                    output = ""
                    output += "<h2>The restaurant " + str(restaurantRecord.name) + " has been updated</h2>"
                    output += "<a href='/restaurants'>Back to the bunch</a>"
                    self.write_output(output)
                    return

                else:
                    self.send_response(301)
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()