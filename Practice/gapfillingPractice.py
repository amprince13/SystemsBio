import cobra.test

from Functions.gapFillFunction import printAndWriteOutput

model = cobra.test.create_test_model("salmonella")

# remove some reactions and add them to the universal reactions
Universal = cobra.Model("Universal_Reactions")
for i in [i.id for i in model.metabolites.f6p_c.reactions]:
    reaction = model.reactions.get_by_id(i)
    Universal.add_reaction(reaction.copy())
    reaction.remove_from_model()
print model.optimize().f

printAndWriteOutput(model, Universal, 3, False)

