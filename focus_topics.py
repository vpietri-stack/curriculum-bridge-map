"""Editorial topic groups for the focused Act 3, PU1, and Play 1 map.

Power Up groups are keyed to consecutive Teacher's Book New language panels.
Every panel has a group, including cross-curricular, literature and exam review.
"""

PU1_PANEL_TOPICS = {
 1: ['School and learning','Position','Position','School and learning','Naming objects','Being kind','Being kind','Classroom story','Classroom story'],
 2: ['Family','Family','Family','Body parts','Body parts','The senses','The senses','Family story','Family story'],
 3: ['Farm animals','Describing animals','Describing animals','Feelings','Describing animals','Animal products','Animal products','Animal story','Animal review'],
 4: ['Food and drink','Food preferences','Food preferences','Food and drink','Food requests','Cooking and ingredients','Cooking and ingredients','Scarecrow story','Scarecrow story','Food review'],
 5: ['Toys and presents','Possession','Possession','Toys and presents','Wants and presents','Shapes','Birthday story','Birthday story'],
 6: ['Town and transport','There is and there are','There is and there are','Zoo animals','Going out','Animal habitats','Animal habitats','Zoo story','Zoo story','Animal review'],
 7: ['Sport and music','Actions now','Actions now','Sport and music','Permission to play','Healthy body','Healthy body','Playground story'],
 8: ['Rooms and furniture','Ability','Days and time','Rooms and furniture','Position','Types of homes','Types of homes','Home story','Home story','Food review'],
 9: ['Clothes','Actions and imperatives','Actions and imperatives','Beach activities','Leisure preferences','Landscapes','Landscapes','Holiday story','Holiday story'],
}

TOPIC_TAGS = {
 'Greetings':'greetings','Colours':'colours','Numbers and age':'numbers',
 'School objects':'school','School and learning':'school','Position':'position','Naming objects':'school','Being kind':'kindness','Classroom story':'rules',
 'Family':'family','Body parts':'body','The senses':'senses','Family story':'family',
 'Farm animals':'animals','Describing animals':'animals','Feelings':'feelings','Animal products':'animals','Animal story':'animals','Animal review':'animals',
 'Food and drink':'food','Food preferences':'food','Food requests':'food','Cooking and ingredients':'food','Scarecrow story':'story','Food review':'food',
 'Toys and presents':'toys','Possession':'possessions','Wants and presents':'toys','Shapes':'shapes','Birthday story':'story',
 'Town and transport':'transport','There is and there are':'places','Zoo animals':'animals','Going out':'places','Animal habitats':'animals','Zoo story':'animals',
 'Sport and music':'leisure','Actions now':'actions','Permission to play':'leisure','Healthy body':'health','Playground story':'leisure',
 'Rooms and furniture':'home','Ability':'ability','Days and time':'time','Types of homes':'home','Home story':'story',
 'Clothes':'clothes','Actions and imperatives':'actions','Beach activities':'leisure','Leisure preferences':'leisure','Landscapes':'nature','Holiday story':'story',
 'Places':'places','Jobs':'jobs','Weather':'weather','Travel':'transport','Directions':'position','Rules':'rules','Shopping':'shopping',
 'Community':'community','Nature':'nature','Descriptions':'descriptions','Stories and review':'story','Opening and review':'story','Phonics':'phonics',
 'Animal actions':'animals','Sequencing':'sequence','Healthy body':'health','Playground':'leisure',
 'School objects':'school','Museum':'places','Dinosaurs':'animals',
}

PU1_WELCOME = [
 {'name':'Colours','tag':'colours','words':'red, blue, yellow, green, orange, purple, pink, grey, black, white, brown','structures':['What colour is it?','It’s (blue).'],'pdfPages':[18,19]},
 {'name':'Numbers and age','tag':'numbers','words':'one, two, three, four, five, six, seven, eight, nine, ten','structures':['How old are you?',"I'm (six)."],'pdfPages':[18,19,20,21]},
 {'name':'Greetings','tag':'greetings','words':'hello, hi, name','structures':['Hello!','Hi!',"What's your name?","I'm (name).",'This is (name).'],'pdfPages':[19,20,21]},
]

# OCR joins words that are separated by a narrow space in the scanned panels.
PU1_OCR_FIXES = {
 'paper playground':'paper, playground','horsepet':'horse, pet','hort':'short','fies':'flies',
 'chicken chocolate':'chicken, chocolate','meat meatballs':'meat, meatballs',
 'plane robot':'plane, robot','teddynew':'teddy, new','lorry motorbike':'lorry, motorbike',
 'hippo lizard':'hippo, lizard','monkeypolarbear':'monkey, polar bear',
 'playbasketball/football/tennis':'play basketball, play football, play tennis',
 'playtheguitar/piano':'play the guitar, play the piano','ridebike':'ride a bike',
 'hiting':'hitting','riding (his)skateboard':'ride a skateboard',
 'muscles strong':'muscles, strong','suncreamvitamin':'sun cream, vitamin',
 'afernoon evening':'afternoon, evening','painting phone':'painting, phone',
 'sof':'sofa','horts':'shorts','shir':'shirt','takephotos':'take photos',
 'waterfll':'waterfall','comedown':'come down','atthe end':'at the end','pick up':'pick up',
 'pickup':'pick up','puton':'put on','lookat':'look at','flya kite':'fly a kite',
 'CanI have...,please?':'Can I have ..., please?',
 'CanI have...,please?I\'m sorry':'Can I have ..., please?, I\'m sorry',
}

PU1_EXTRA_PATTERNS = {
 (1,'Being kind'):['Are you OK?','Yes, thank you.','Here you are.','Thank you.','Please help.','Let us share.','Work together.'],
 (2,'The senses'):['I can see / hear / smell / taste / touch.'],
 (4,'Food requests'):['Can I have some (chocolate), please?','Here you are.'],
 (6,'Animal habitats'):['Where do (penguins) live?','They live in (cold places).'],
 (7,'Healthy body'):['Stretch your muscles.','Exercise and eat a healthy diet.'],
 (9,'Actions and imperatives'):['Look at the picture.','Pick up the (bag).','Put on the (hat).'],
}

# Topics for the TLS sessions. A session may contribute to more than one card
# when its vocabulary and sentence patterns cover different subjects.
ISHOW_TOPIC_ORDER = {
 'IS-Act3-1':['Greetings','Places','Jobs','Phonics'],
 'IS-Act3-2':['Places','School objects','Rules','Colours','Descriptions','Phonics'],
 'IS-Act3-3':['Playground','Numbers and age','Phonics'],
 'IS-Act3-4':['Days and time','Weather','Travel','Phonics'],
 'IS-Act3-5':['Toys and presents','Shopping','Numbers and age','Phonics'],
 'IS-Act3-6':['Travel','Beach activities','Nature','Descriptions','Phonics'],
 'IS-Act3-7':['Travel','Zoo animals','Animal actions','Shopping','Phonics'],
 'IS-Act3-8':['Food and drink','Food requests','Cooking and ingredients','Sequencing','Phonics'],
 'IS-Act3-9':['Travel','Dinosaurs','Museum','Phonics'],
 'IS-Play1-1':['Greetings','Numbers and age','Family','Phonics'],
 'IS-Play1-2':['School objects','Naming objects','Phonics'],
 'IS-Play1-3':['Nature','Colours','Numbers and age','Descriptions','Phonics'],
 'IS-Play1-4':['Food and drink','Food preferences','Healthy body','Phonics'],
 'IS-Play1-5':['Toys and presents','Possession','Descriptions','Phonics'],
 'IS-Play1-6':['Travel','Places','Colours','Phonics'],
 'IS-Play1-7':['Zoo animals','Animal actions','Phonics'],
 'IS-Play1-8':['Position','Zoo animals','Nature','Colours','Phonics'],
 'IS-Play1-9':['Weather','Clothes','Possession','Phonics'],
}

TOPIC_TAGS.update({'Playground':'leisure','Animal actions':'animals','Sequencing':'sequence','Dinosaurs':'animals','Museum':'places'})
