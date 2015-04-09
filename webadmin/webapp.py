# coding:utf-8
import json

from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis


class IndexHandler(BaseHandler):
    def get(self):
        self.render("index.html")


class ListHandler(BaseHandler):
    def get(self):
        page_size = self.get_argument("length", 30)
        group = self.get_argument("group", 1)
        draw = self.get_argument('draw', 1)
        start = self.get_argument("start", 0)
        total = self.db.query("select count(1) as cnt from base")[0]['cnt']

        if int(group) == 1:
            cates = (979, 1001, 974, 998, 976, 996, 978, 1000, 977, 999, 984, 1006, 985, 1007, 975, 997)
        else:
            cates = (982, 1004, 981, 1003, 990, 1012)

        raw_sql = """
        SELECT b.id, b.title, b.zone, b.publish_time, b.url, group_concat( concat_ws( '##', a.name, a.id )
        SEPARATOR '###' ) AS atts
        FROM base AS b
        LEFT JOIN attachments AS a ON b.id = a.base_id
        where b.category in ("""+','.join(cates)+""")
        GROUP BY b.id
        ORDER BY b.publish_time DESC
        LIMIT %s , %s
        """
        data = self.db.query(raw_sql, int(start), int(page_size))
        result = {'draw': draw, 'recordsFiltered': total,
                  'recordsTotal': total, 'data': data}

        self.write(json.dumps(result))


class DetailHandler(BaseHandler):
    def get(self):
        bid = self.get_argument("bid")
        item = self.db.query('select title, publish_time, zone, content from base where id = %s', bid)
        self.render("detail.html", item=item[0])


class DownloadHandler(BaseHandler):
    def get(self):
        aid = self.get_argument("aid")
        item = self.db.query('select name, file from attachments where id = %s', aid)
        self.set_header('Content-Type', 'application/octet-stream; charset="utf-8"')
        self.set_header('Content-Disposition', 'attachment; filename="%s"' % item[0]['name'])
        self.write(item[0]['file'])
