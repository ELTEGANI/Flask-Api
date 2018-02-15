from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item (Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
     type=float,
     required=True,
     help="this filed cannot be empty")
    parser.add_argument('store_id',
      type=int,
      required=True,
      help="Every needs item store id")

    @jwt_required()
    def get(self,name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return item.json()
        return {'message':'item not found'},404



    def post(self,name):
        if ItemModel.find_item_by_name(name):
           return {'meassge':"An item with name '{}' already exists".format(name)}, 400
        data  = Item.parser.parse_args()
        item  = ItemModel(name ,data['price'],data['store_id'])
        try:
           item.save_to_db()
        except:
           return {"message":"Error Occurred while inserting item."},500
        return item.json(), 201


    def delete (self,name):
     item = ItemModel.find_item_by_name(name)
     if item:
         item.delete_from_db()
     return {'message':'item deleted'}

    def put (self,name):
        data  = Item.parser.parse_args()
        item = ItemModel.find_item_by_name(name)
        if item is None:
            item = ItemModel(name,data['price'],data['store_id'])
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()




class Itemlist(Resource):
      def get(self):
          return {'item':[x.json() for x in ItemModel.query.all()]}
