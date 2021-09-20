# M2_cloudComputing_bicycle


4 mini projets : 
1. récupérer quelques villes, les formater (chaque ville aura sa propre structure)
2. refresh régulier
3. vélos dispo, proche de ce qu'on avait fait mais avec filtre vélo dispo
4. plus de trucs

projet en python, avec marc, hébergé sur git (envoy par mail), deux semaines (rendu à la fin du cours du lundi 27)


**Lille** => données ok
https://opendata.lillemetropole.fr/explore/dataset/vlille-realtime/api/

https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=400&facet=nom&facet=type&facet=nbvelosdispo&facet=nbplacesdispo => data geojson / facet permet de préciser champs à avoir (?)
https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion => data geojson

contient :
"datasetid":"vlille-realtime",
"recordid":"e5decefb7f404a94fafd43a439835a1c6555f661",
"fields":{
    "etat":"EN SERVICE",
    "etatconnexion":"CONNECTED",
    "nbvelosdispo":0,
    "nbplacesdispo":0,
    "commune":"VILLENEUVE D'ASCQ",
    "type":"AVEC TPE",
    "libelle":129,
    "datemiseajour":"2019-10-21T07:46:05+00:00",
    "localisation":[
        50.63608,
        3.130853
    ],
    "nom":"FLERS CHATEAU",
    "adresse":"RUE DE LA CHEVALERIE",
    "geo":[
        50.63608,
        3.130853
    ]
},
"geometry":{
    "type":"Point",
    "coordinates":[
        3.130853,
        50.63608
    ]
},
"record_timestamp":"2021-09-17T08:39:01.532000+00:00"

transformations :
- filtrer nbvelosdispo, nbplacesdispo, type, nom, geometry
- transformer type en booléen (0 pour "SANS TPE", 1 pour "AVEC TPE")
- créer champs : 
    - nbvelosdispo + nbplacesdispo => nbplacestotal
    - ville => lille
- renommer champs : 
    - type => cb


**Montpellier** => données ok
https://data.opendatasoft.com/explore/dataset/disponibilite-des-places-velomagg-en-temps-reel%40occitanie/api/?flg=fr&lang=&rows=10

https://data.opendatasoft.com/api/records/1.0/search/?dataset=disponibilite-des-places-velomagg-en-temps-reel%40occitanie&q=&rows=100 => data json avec coord

contient :
- Id : identifiant de la station
- La : latitude
- Lg : longitude
- Av : nombre de places occupées
- Fr : nombre de places libres
- To : nombre total de places
- Cb : lecteur de carte bancaire disponible (0 pour non, 1 pour oui)
- Na : nom

exemple :
"datasetid": "disponibilite-des-places-velomagg-en-temps-reel@occitanie",
"recordid": "a72ed4cb96da76744bf01b59710396687aacef2e", 
"fields": {
    "lg": 3.878778, 
    "fr": 12, 
    "la": 43.608148, 
    "na": "002 Com\u00e9die", 
    "to": 24, 
    "av": 12, 
    "id": "002"
}, 
"record_timestamp": "2021-09-17T08:30:26.564000+00:00"

transformations :
- filtrer fr, av, to, cb (???), na, lg, la
- créer champs :
    - ville => montpellier
    - geometry => combine lg et la
- renommer champs : 
    - fr => nbplacesdispo
    - av => nbvelosdispo
    - to => nbplacestotal
    - na => nom
- supprimer champs lg et la


**Lyon** => données ok
https://data.grandlyon.com/jeux-de-donnees/amenagements-cyclables-metropole-lyon/api
https://www.data.gouv.fr/fr/datasets/activite-des-stations-velov-du-quartier-confluence-a-lyon/#

https://download.data.grandlyon.com/wfs/grandlyon?SERVICE=WFS&VERSION=2.0.0&request=GetFeature&typename=pvo_patrimoine_voirie.pvostationvelov&outputFormat=application/json;%20subtype=geojson&SRSNAME=EPSG:4171&startIndex=0 => data geojson (more)
https://download.data.grandlyon.com/wfs/rdata?SERVICE=WFS&VERSION=2.0.0&request=GetFeature&typename=jcd_jcdecaux.activitejcdvelov&outputFormat=geojson&SRSNAME=EPSG:2154 => data geojson (less)


fusion de deux sources : 
https://transport.data.gouv.fr/gbfs/lyon/station_information.json => fixe

exemple :
"address":"ANGLE ALLEE ANDRE MURE ET QUAI ANTOINE RIBOUD",
"capacity":22,
"lat":45.743317,
"lon":4.815747,
"name":"2010 - CONFLUENCE / DARSE",
"station_id":"2010"

transformations :
- filtrer capacity, name, lat, lon, station id
- transformer name (substring)
- creer champs :
    - ville => lyon
    - geometry => combine lat et lon
    - nbvelosdispo => 0
    - nbplacesdispo => 0
- renommer champs :
    - capacity => nbplacestotal
    - name => nom
- supprimer champs lat et lon


https://transport.data.gouv.fr/gbfs/lyon/station_status.json => refresh

exemple :
"is_installed":1,
"is_renting":1,
"is_returning":1,
"last_reported":1631870457,
"num_bikes_available":5,
"num_docks_available":17,
"station_id":"2010"

transformations :
- filtrer num_bikes_available, num_docks_available, station_id
- modifier valeurs pour station id en bdd:
    - nbvelosdispo => num_bikes_available
    - nbplacesdispo => num_docks_available


**god mod**
solution ultime : https://developer.jcdecaux.com/#/opendata/vls?page=dynamic



**elements pour q4**
1 - index sur nom (voire ville)
2 - modif de champs (libre ou imposé) => 1 seul
3 - supprimer une ou toutes les entrées de table live ? ou history ? ou données "anciennes de history" ? => suppression d'une ou plusieurs stations + historique / éventuellement purge d'historique
4 - desactivate ?? => trouvable / pas trouvable pour le 1 => tous ou partie => sélection de zone par polygone
5 - utiliser fonctions mongo => se renseigner
