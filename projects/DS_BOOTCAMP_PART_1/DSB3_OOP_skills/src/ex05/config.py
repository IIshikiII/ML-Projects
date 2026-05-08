report_template = (
    "We made {observations_number} observations by tossing a coin: "
    "{tails} were tails and {heads} were heads. The "
    "probabilities are {tails_ratio:.2} and {heads_ratio:.2}, respectively. "
    "Our forecast is that the next {n} "
    "observations will be: {tails_pred} tail and {heads_pred} heads."
)
n = 3
data_file_name = "data.csv"
save_file_name = "output"
save_file_extention = "txt"
