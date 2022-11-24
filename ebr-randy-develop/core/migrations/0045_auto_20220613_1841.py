# Generated by Django 3.2.12 on 2022-06-13 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_auto_20220613_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Additional_Motors',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Battery',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Battery_Watt_Hrs',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Belt_Drive',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Brake_Type',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Brand',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Cassette',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Chainring',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Charger',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Class',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Continually_Variable_Transmission',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Crankset',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Display',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Electronic_Shifting',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Fenders',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Fork',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Frame',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Frame_Type',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Front_Brake',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Front_Derailleur',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Front_Hub',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Front_Rack',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Front_Wheel',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Gears',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Grips',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Handlebar',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Headset',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Internally_Geared_Hub',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Lights',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Load_Capacity',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='MSRP',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Model',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Motor',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Motor_Nominal_Output',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Motor_Type',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Pedals',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Rear_Brake',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Rear_Derailleur',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Rear_Hub',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Rear_Rack',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Rear_Shock',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Rear_Wheel',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Saddle',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Seatpost',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Seatpost_Diameter',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Shift_Levers',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Smart_Bike',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Stem',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Suspension',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Theft_GPS',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Tires',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Trim',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='URL',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Weight',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Wheel_Size',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv1',
            name='Year',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='All_Mountain_Enduro',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='All_Other_Cargo',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='All_Other_Fat',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='All_Other_Mountain',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='All_Other_Road',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='All_Other_Trike',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Box_Bike',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Cargo',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='City',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Commuting',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Cross_Country',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Cruiser',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Delta',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Drop_Bars',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Fat',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Folding',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Freeride_Downhill',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Gravel',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Hunting',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Kids',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Minibike',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Mountain',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Other',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Recumbent',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Road',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Tadpole',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Trail',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Trike',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='URL',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv2',
            name='Utility',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Accessories',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Attachment_Points',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Availability',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Battery_Chemistry',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Battery_Weight',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Brake_Details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Charge_Time',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Display_Accessories',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Display_Readouts',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Drive_Mode',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Drive_Mode_Details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Estimated_Max_Range',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Estimated_Min_Range',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Frame_Colors',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Frame_Sizes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Geometry_Measurements',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Motor_Output_Peak',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Motor_Torque',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Motor_Weight',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Other',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Seatpost_Length',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Spokes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Suggested_Use',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Tire_Details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Top_Speed',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Tube_Details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='URL',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewcsv3',
            name='Warranty',
            field=models.TextField(blank=True, null=True),
        ),
    ]
