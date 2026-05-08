from config import *
from analytics import Research

try:
    class_obj = Research(data_file_name)
    data = class_obj.file_reader(has_header=True)

    calculations = class_obj.Calculations(data)
    heads, tails = calculations.counts()
    heads_ratio, tails_ratio = calculations.fractions(heads, tails)

    analytics_obj = class_obj.Analytics(data)
    predictions = analytics_obj.predict_random(n)
    pred_calculations = class_obj.Calculations(predictions)
    pred_heads, pred_tails = pred_calculations.counts()

    output = report_template.format(
        observations_number=class_obj.observations_number,
        tails=tails,
        heads=heads,
        tails_ratio=tails_ratio,
        heads_ratio=heads_ratio,
        n=n,
        tails_pred=pred_tails,
        heads_pred=pred_heads,
    )

    analytics_obj.save_file(output, save_file_name, save_file_extention)


except FileNotFoundError:
    print("This file doesn't exist.")
