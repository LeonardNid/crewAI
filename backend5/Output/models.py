class Frame(db.Model):
    __tablename__ = 'frames'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)
    brand = db.Column(db.String)
    material = db.Column(db.String)
    maximum_tire_width = db.Column(db.String)
    compatible_brakes = db.Column(db.PickleType, default=[])  # Initialized as empty list
    compatible_gears = db.Column(db.PickleType, default=[])  # Initialized as empty list
    drivetrain_type = db.Column(db.Enum('hub', 'chain'))
    frame_type = db.Column(db.Enum('gravel', 'road bike', 'touring bike', 'city bike'))
    specific_properties = db.Column(db.String)
    price = db.Column(db.Float)
    weight = db.Column(db.Float)
    geometry = db.Column(db.String)
    compatible_handlebars = db.Column(db.PickleType, default=[])  # Initialized as empty list
    max_carry_weight = db.Column(db.Float)
    compatible_seatposts = db.Column(db.PickleType, default=[])  # Initialized as empty list
    cable_routing_type = db.Column(db.Enum('external', 'internal'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'material': self.material,
            'maximum_tire_width': self.maximum_tire_width,
            'compatible_brakes': self.compatible_brakes,
            'compatible_gears': self.compatible_gears,
            'drivetrain_type': self.drivetrain_type,
            'frame_type': self.frame_type,
            'specific_properties': self.specific_properties,
            'price': self.price,
            'weight': self.weight,
            'geometry': self.geometry,
            'compatible_handlebars': self.compatible_handlebars,
            'max_carry_weight': self.max_carry_weight,
            'compatible_seatposts': self.compatible_seatposts,
            'cable_routing_type': self.cable_routing_type
        }
