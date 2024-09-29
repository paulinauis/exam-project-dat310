Vi bruker SQLite database til å lagre informasjon, css til layout og JS til frontend. 

Du starter applikasjonen ved å først kjøre setup_db.py og så app.py. Vi bruker fire tabeller: admins for administartorer, posts for innlegg, subscriptions for nyhetsbrev og users for brukere. Vi begynner med fire administratorer (som også er brukere), en vanlig bruker og tre innlegg. Alle brukere er med i nyhetsbrev. 

Header: 
- Hvis du trykker inn på logoen eller hjem-ikonet så kommer du deg til startsiden 
- Hvis du trykker inn på "Logg inn"- eller "Registrer"-knappen så kommer du videre til innlogging- eller registreringssiden. 
- Under "Meny" finner du de ulike sidene (startsiden, alle innlegg, side om alle fire administratorer, og side med kontaktinformasjon)
- Om du er innlogget, vises "Velkommen, og så navnet på brukeren". Om du er innlogget som bruker, forsvinner registreringsknappen. Om du er innlogget som administrator så kan du gå inn på "Opprett innlegg" for å skrive et nytt innlegg

Footer: 
- Hvis du trykker deg inn på logoen så kommer du deg til startsiden
- Hvis du trykker inn på "Om oss" så kommer du deg til fellessiden om alle administratorer, og hvis du trykker på et navn så kommer du deg inn på siden om vedkommende 
- Facebook- og Instagram-siden er linket under "Våre sosiale medier"
- Om du skriver inn e-post adressen din under "Subscribe" og trykker på "Abonner", blir mailen lagret i subscribe-tabellen. 

Inne på startsiden: 
- "Hvem vi er"-knappen fører deg til siden om alle administratorer 
- Du kan trykke på pilene i slideshow for å se bilder av alle administratorer, samt trykke på bildet for å komme deg videre til siden om vedkommende 
- Under "Hva vi gjør", kan du også trykke på hver administrator for å komme deg videre til siden om vedkommende 
- Under "Siste oppdatering" får du opp siste publiserte innlegg

Logg inn-skjemaet: 
- Du får opp en feilmelding dersom du ikke skriver inn e-post addressen og/eller passordet 
- Om mailen ikke finnes i databasen eller passordet er feil, forblir du på innloggingsiden. Om både mail og passord stemmer og finnes i databasen blir du redirectet til startsiden. 
- Du kan teste ut innloggingen som vanlig bruker med dorte@gmail.com / dorte1234 eller som admin med f.eks. sofie@gmail.com / sofie1234.

Innlegg-siden
- Som bruker kan du lese innlegg, samt søke på ord i innlegg
- Som administartor kan du i tillegg slette og redigere innlegg
- Innleggene er vist kronologisk, dvs nyeste øverst på siden

Om oss-siden
- Her kan du trykke deg inn på bilde av hver administartor for å komme deg videre til siden om vedkommende 

Kontakt-siden
- Facebook og Instagram er linket 

Det finnes også en mobilversjon av siden som ble testet på 760px i bredde


Kilder til bildene: 
- logo: https://www.freepik.com/premium-vector/logo-text-here-slogan-here-design-art-template_28405304.htm 
- sofie: https://nn.wikipedia.org/wiki/Lama 
- paulina: https://desenio.no/p/posters-og-plakater/svart-og-hvitt/lama-bw-plakat/ 
- anette: https://www.europosters.no/marketplace/alpaka-lama-animal-v132754 
- lisbeth: https://unsplash.com/photos/a-close-up-of-an-alpaca-looking-at-the-camera-SyX853fa1vs
- fargegata: https://www.visitnorway.no/reisemal/vestlandet/stavangerregionen/
- preikestolen: https://no.tripadvisor.com/Tourism-g190511-Stavanger_Stavanger_Municipality_Rogaland_Western_Norway-Vacations.html
