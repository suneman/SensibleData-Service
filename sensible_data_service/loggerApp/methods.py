# log_entry = <flowID, D, C, Y>
# D = <userID,appID,payload>
def append_dataFlow(self, data):
	current_flowID = self.logDatabase.getMaxFlowID() + 1    
	current_D = helperModule.create_D(data)
	current_C = helperModule.create_C(current_D)
	previous_Y = self.logDatabase.getEntry(current_flowID - 1).get("Y")
	current_Y = helperModule.create_Y(previous_Y, current_C)
	self.logDatabase.writeEntry(current_flowID, current_D, current_C, current_Y)    # Finally, writes the log entry
	return current_flowID

