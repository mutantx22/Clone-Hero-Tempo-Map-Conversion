# Clone-Hero-Tempo-Map-Conversion
Convert notes between 2 different tempo maps in moonscraper

# How to use

1. In "bpm-resolution-dual-maps.py"  change the values of
   OLD_RESOLUTION = 480
   NEW_RESOLUTION = 480
   to whatever value your song needs to be
    

2. open up the .chart file in a text editor with the old tempo map you want to replace and
   Copy the number values under "SyncTrack" of the old tempo map
   <img width="610" height="600" alt="2026-05-05_232706" src="https://github.com/user-attachments/assets/c98e0cfc-e59d-4972-baa9-7c23afda69f7" />


3. Paste the number values in "old_sync.txt"  of the old tempo map
   <img width="374" height="430" alt="2026-05-05_232755" src="https://github.com/user-attachments/assets/d284eeda-0525-4968-8866-156a92ae6368" />

4. Copy the number values under "SyncTrack" of the new tempo map you wish to use
   <img width="343" height="593" alt="2026-05-05_232857" src="https://github.com/user-attachments/assets/3df0b63b-7d33-4979-8be6-ff32cd8d0772" />

5. Paste the number values in "new_sync.txt"  of the new tempo map  you wish to use
   <img width="276" height="628" alt="2026-05-05_232935" src="https://github.com/user-attachments/assets/68c28a1b-5adf-4c58-a468-6e7c9b969be3" />

6. Copy the note values under ExpertSingle
   <img width="232" height="559" alt="2026-05-05_234237" src="https://github.com/user-attachments/assets/4b9f8f91-db46-4f83-bb3b-84108cbfa316" />

7. Paste the note values in  "expert.txt"
   <img width="346" height="632" alt="2026-05-05_234525" src="https://github.com/user-attachments/assets/680c590b-35d6-4c61-87e4-ccd39c778bd3" />

8. Run the script using:
   ``python bpm-resolution-dual-maps.py

   <img width="976" height="511" alt="2026-05-05_234821" src="https://github.com/user-attachments/assets/a6dbabab-e897-4558-b410-932dd4e1b1b2" />

