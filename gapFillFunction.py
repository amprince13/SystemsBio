from cobra.io.sbml import create_cobra_model_from_sbml_filefrom cobra import Model, Reaction, flux_analysisfrom uniqAndSort import uniq, sort_and_deduplicateimport reimport timestart_time = time.time()import operatorfrom copy import deepcopy# This function gapfills the model using the growMatch algorithm that is built into cobrapie# It takes three inputs: a model in SMBL format, a database of reactions and the number of runs# that the growMatch algorithm should run throughdef gapFillFunc(model, database, runs):    # Creates the model from smbl file and then creates a model object (Universal) in which the reactions from    # the database are stored and can be added into the model for gapfilling    funcModel = create_cobra_model_from_sbml_file(model)    Universal = Model("Universal Reactions")    f = open(database, 'r')    next(f)    rxn_dict = {}    # Creates a dictionary of the reactions from the tab delimited database, storing their ID and the reaction string    for line in f:        rxn_items = line.split('\t')        rxn_dict[rxn_items[0]] = rxn_items[6]    # Adds the reactions from the above dictionary to the Universal model    for rxnName in rxn_dict.keys():        rxn = Reaction(rxnName)        Universal.add_reaction(rxn)        rxn.reaction = rxn_dict[rxnName]    growthValue = []    result = flux_analysis.growMatch(funcModel, Universal, iterations=runs)    resultShortened = sort_and_deduplicate(uniq(result))    rxns_added = {}    print resultShortened    for x in range(len(resultShortened)):        funcModelTest = deepcopy(funcModel)        for i in range(len(resultShortened[x])):            addID = resultShortened[x][i].id            rxn = Reaction(addID)            funcModelTest.add_reaction(rxn)            rxn.reaction = resultShortened[x][i].reaction            rxn.reaction = re.sub('\+ dummy\S+', '', rxn.reaction)            print rxn.reaction        solution = funcModelTest.optimize()        growthValue.append(solution.f)        print findInsAndOuts(funcModelTest)    funcModelTest = deepcopy(funcModel)    for i in range(len(resultShortened)):        rxns_added[i] = resultShortened[i], growthValue[i]    return rxns_addeddef printAndWriteOutput(model, database, runs, writeCommand, writeFile='gapFillOuput.txt'):    f = open(writeFile, 'w')    rxns_added = gapFillFunc(model, database, runs)    print rxns_added    for key in rxns_added.keys():        print "-------------------------------"        print "Run Number: " + str(key)        print "-------------------------------"        for i in range(len(rxns_added[key][0])):            rxn_name = re.sub('\+ dummy\S+', '', rxns_added[key][0][i].reaction)            print "%s : %s" % (rxns_added[key][0][i].id, rxn_name)        print "-------------------------------"        print "Objective function value: " + str(rxns_added[key][1])        print "-------------------------------"        print "Major in fluxes"        for i in range(len(rxns_added[key][2])):            print str(rxns_added[key][2][i][0]) + ": " + str(rxns_added[key][2][i][1])        print "-------------------------------"        print "Major out fluxes"        for i in range(len(rxns_added[key][3])):            print str(rxns_added[key][3][i][0]) + ": " + str(rxns_added[key][3][i][1])        print "-------------------------------"    time_final = time.time()    print "Time to run: " + str(time_final - start_time)    # if writeCommand == True:    #     for key in rxns_added.keys():    #         f.write("-------------------------------\n")    #         f.write("Run Number: " + str(key) + '\n')    #         f.write("-------------------------------\n")    #         for i in range(len(rxns_added[key][0])):    #             rxn_name = re.sub('\+ dummy\S+', '', rxns_added[key][0][i].reaction)    #             f.write("%s : %s" %(rxns_added[key][0][i].id, rxn_name) + '\n')    #         f.write("-------------------------------\n")    #         f.write("Objective function value: " + str(rxns_added[key][1]) + '\n')    #         f.write("-------------------------------\n")    #         f.write("Major in fluxes\n")    #         for i in range(len(rxns_added[key][2])):    #             f.write(str(rxns_added[key][2][i][0]) + ": " + str(rxns_added[key][2][i][1])+'\n')    #         f.write("-------------------------------\n")    #         f.write("Major out fluxes\n")    #         for i in range(len(rxns_added[key][3])):    #             f.write(str(rxns_added[key][3][i][0]) + ": " + str(rxns_added[key][3][i][1]) + '\n')    #         f.write("-------------------------------\n")    #     f.write("Time to run: " + str(time_final - start_time) +'\n')    else:        passdef findInsAndOuts(model):    testModel = model.copy()    testModel.optimize()    threshold = 1E-8    out_rxns = testModel.reactions.query(        lambda rxn: rxn.x > threshold, None    ).query(lambda x: x, 'boundary')    in_rxns = testModel.reactions.query(        lambda rxn: rxn.x < -threshold, None    ).query(lambda x: x, 'boundary')    in_fluxes = {}    out_fluxes = {}    for rxn in in_rxns:        in_fluxes[rxn.name] = rxn.x    for rxn in out_rxns:        out_fluxes[rxn.name] = rxn.x    sorted_out = sorted(out_fluxes.items(), key=operator.itemgetter(1), reverse=True)    sorted_in = sorted(in_fluxes.items(), key=operator.itemgetter(1), reverse=False)    return sorted_out, sorted_in