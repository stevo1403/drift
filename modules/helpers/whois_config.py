config = [
	{
		'target':{
		'FIELD_NAME':{'words':[['Domain', 'Name']]}
		},
		'action':'replace',
		'key':'data.Domain_Name',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Domain', 'Status']]}
		},
		'action':'append',
		'key':'data.Domain_Status',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Registrar', 'Server'], ['WHOIS', 'Server'], ]}
		},
		'action':'append',
		'key':'data.Registrar.WHOIS_Server',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Name', 'Server']]}
		},
		'action':'append',
		'key':'data.Name_Server',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Domain', 'ID']]}
		},
		'action':'replace',
		'key':'data.Domain_ID',
	},

	{
		'target':{
		'FIELD_NAME':{'words':[['Registrant', 'ID']]}
		},
		'action':'replace',
		'key':'data.Registrant.ID',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Registrant', 'Name']]}
		},
		'action':'replace',
		'key':'data.Registrant.Name',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Registrant', 'Organization']]}
		},
		'action':'replace',
		'key':'data.Registrant.Organization',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Registrant', 'Street']]}
		},
		'action':'append',
		'key':'data.Registrant.Street',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Registrant', 'City']]}
		},
		'action':'replace',
		'key':'data.Registrant.City',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Registrant', 'State']]}
		},
		'action':'replace',
		'key':'data.Registrant.State',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Registrant', 'Postal Code'], ['Registrant', 'Postal'], ]}
		},
		'action':'replace',
		'key':'data.Registrant.Postal_Code',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Registrant', 'Country'], ['Registrant', 'Nation'], ['Registrant', 'Nationality'], ]}
		},
		'action':'replace',
		'key':'data.Registrant.Country',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Registrant', 'Phone'], ]}
		},
		'action':'append',
		'key':'data.Registrant.Phone',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Registrant', 'Email'], ]}
		},
		'action':'append',
		'key':'data.Registrant.Email',
	},


	{
		'target':{
		'FIELD_NAME':{'words':[['Billing', 'ID']]}
		},
		'action':'replace',
		'key':'data.Billing.ID',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Billing', 'Name']]}
		},
		'action':'replace',
		'key':'data.Billing.Name',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Billing', 'Organization']]}
		},
		'action':'replace',
		'key':'data.Billing.Organization',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Billing', 'Street']]}
		},
		'action':'replace',
		'key':'data.Billing.Street',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Billing', 'City']]}
		},
		'action':'replace',
		'key':'data.Billing.City',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Billing', 'Postal Code'], ['Billing', 'Postal'], ]}
		},
		'action':'replace',
		'key':'data.Billing.Postal_Code',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Billing', 'Country'], ['Billing', 'Nation'], ['Billing', 'Nationality'], ]}
		},
		'action':'replace',
		'key':'data.Billing.Country',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Billing', 'Phone'], ]}
		},
		'action':'append',
		'key':'data.Billing.Phone',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Billing', 'Email'], ]}
		},
		'action':'append',
		'key':'data.Billing.Email',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['DNSSEC'], ['Domain Name System Security']]}
		},
		'action':'replace',
		'key':'data.DNSSEC',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['DATE', 'UPDATE'], ['DATE', 'UPDATED'], ['DATE', 'MODIFIED'], ['DATE', 'ALTER'], ['LAST', 'UPDATED'],]}
		},
		'action':'replace',
		'key':'data.Updated_Date',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['DATE', 'UPDATE'], ['DATE', 'CREATED'], ['DATE', 'CREATE'], ['DATE', 'REGISTER'], ['DATE', 'CREATION'],]}
		},
		'action':'replace',
		'key':'data.Created_Date',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['DATE', 'EXPIRE'], ['DATE', 'EXPIRATION'], ['DATE', 'EXPIRY'], ['DATE', 'DELETED'], ['DATE', 'DELETION'],]}
		},
		'action':'replace',
		'key':'data.Expiration_Date',
	},
	
	{
		'target':{
		'FIELD_NAME':{'words':[['Registrar', 'Email', 'Abuse']]}
		},
		'action':'append',
		'key':'data.Registrar.Abuse_Email',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Registrar', 'Phone', 'Abuse']]}
		},
		'action':'append',
		'key':'data.Registrar.Abuse_Phone',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['IANA', 'ID']]}
		},
		'action':'replace',
		'key':'data.Registrar.IANA_ID',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Registrar', 'URL']]}
		},
		'action':'append',
		'key':'data.Registrar.URL',
	},
	{
		'target':{
		'FIELD_NAME':{'texts':['Registrar','Registrar Name']}
		},
		'action':'append',
		'key':'data.Registrar.Name',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Registrar', 'Customer', 'Email'], ['Registrar', 'Support', 'Email'], ['Registrar', 'Service', 'Email'], ]}
		},
		'action':'replace',
		'key':'data.Registrar.Customer_Service_Email',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Registrar', 'Customer', 'Contact'], ['Registrar', 'Support', 'Contact'], ['Registrar', 'Service', 'Contact'], ]}
		},
		'action':'replace',
		'key':'data.Registrar.Customer_Service_Contact',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Registrar', 'Admin', 'Contact'], ['Registrar', 'Administrator', 'Contact'], ]}
		},
		'action':'replace',
		'key':'data.Registrar.Admin_Contact',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Registrar', 'Admin', 'Email'], ['Registrar', 'Administrator', 'Email'], ]}
		},
		'action':'replace',
		'key':'data.Registrar.Admin_Email',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Registrar', 'Country']]}
		},
		'action':'replace',
		'key':'data.Registrar.Country',
	},
	{
		'target':{
		'FIELD_NAME':{'words':[['Registrar', 'Phone']]}
		},
		'action':'replace',
		'key':'data.Registrar.Phone',
	},
	
	{
		'target':{
		'FIELD_NAME':{'words':[['ICANN', 'WHOIS', 'URL', 'Complaint'], ['ICANN', 'WHOIS', 'URL', 'Form'], ['ICANN', 'WHOIS', 'URL', 'Inaccuracy']]}
		},
		'action':'replace',
		'key':'data.Registrar.Complaint_URL',
	},

	{
		'target':{
		'FIELD_NAME':{'words':[['ICANN', 'WHOIS', 'Reporting', 'URL'], ['URL', 'Reporting	']]}
		},
		'action':'replace',
		'key':'data.Registrar.Report_URL',
	},
]
