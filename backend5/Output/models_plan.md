### Database Schema

1. **Frame**
   - id: integer (Primary Key, Auto-increment)
   - name: string (Unique)
   - brand: string
   - material: string
   - maximum_tire_width: string
   - compatible_brakes: array (Foreign Key to `Brakes.id`)
   - compatible_gears: array (Foreign Key to `Gears.id`)
   - drivetrain_type: string (Enum: 'hub', 'chain')
   - frame_type: string (Enum: 'gravel', 'road bike', 'touring bike', 'city bike')
   - specific_properties: string (Description of specific properties per frame type)
   - price: float
   - weight: float
   - geometry: string
   - compatible_handlebars: array (Foreign Key to `Handlebars.id`)
   - max_carry_weight: float
   - compatible_seatposts: array (Foreign Key to `Seatposts.id`)
   - cable_routing_type: string (Enum: 'external', 'internal')

2. **Rim**
   - id: integer (Primary Key, Auto-increment)
   - tire_width: string
   - compatible_tire_types: array (string)
   - rim_height: float
   - weight: float
   - price: float
   - required_valve_length: string
   - material: string
   - compatible_frames: array (Foreign Key to `Frame.id`)
   - brand: string

3. **Brakes**
   - id: integer (Primary Key, Auto-increment)
   - type: string (Enum: 'hydraulic', 'mechanical')
   - weight: float
   - price: float
   - brand: string
   - compatible_frames: array (Foreign Key to `Frame.id`)
   - compatible_gears: array (Foreign Key to `Gears.id`)

4. **Gears**
   - id: integer (Primary Key, Auto-increment)
   - type: string (Enum: 'electronic', 'mechanical')
   - weight: float
   - price: float
   - brand: string
   - compatible_frames: array (Foreign Key to `Frame.id`)
   - compatible_brakes: array (Foreign Key to `Brakes.id`)

5. **Handlebars**
   - id: integer (Primary Key, Auto-increment)
   - type: string (Enum: 'flat', 'road', 'gravel', 'mountain bike')
   - material: string
   - weight: float
   - brand: string
   - compatible_frames: array (Foreign Key to `Frame.id`)
   - compatible_brakes: array (Foreign Key to `Brakes.id`)
   - compatible_gears: array (Foreign Key to `Gears.id`)
   - price: float

6. **Saddle**
   - id: integer (Primary Key, Auto-increment)
   - type: string (Description of the type)
   - shape: string
   - compatible_seatposts: array (Foreign Key to `Seatposts.id`)
   - brand: string
   - price: float
   - weight: float

7. **Seatpost**
   - id: integer (Primary Key, Auto-increment)
   - material: string
   - compatible_frames: array (Foreign Key to `Frame.id`)
   - brand: string
   - price: float
   - weight: float
   - compatible_seatposts: array (Foreign Key to `Seatposts.id`)

8. **BrakePad**
   - id: integer (Primary Key, Auto-increment)
   - brake_type: string (Enum: 'disc', 'rim')
   - compatible_brakes: array (Foreign Key to `Brakes.id`)
   - brand: string
   - price: float

### Relationships:
- Each **Frame** can be compatible with multiple **Brakes**, **Gears**, **Handlebars**, and **Seatposts**.
- Each **Rim** can be compatible with multiple **Frames**.
- **Brakes** and **Gears** can be combined but also referenced separately for compatibility.
- **Handlebars** and **Saddles** have specific compatibility requirements with their respective components.

This schema allows for inventory management of the bicycle workshop and facilitates complex queries for compatible parts based on various bike configurations.