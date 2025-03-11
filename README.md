This tool act as a library of asset. But can be adapted for project or some other content depending how you set up the configuration file.
This is a project from 3-4 years ago started during my Artfx School as personal project to present. The code needs a global refactorisation now as it have been developped fast as a "proof of concep"t or "tool to present" and so accumulated technical debt. 
I'm using it for my personal CGU/Motion design project and I now need to improve it. Here are the next step I need to do before next feature : 
 - 1 Develop unit test for, at least, the most important feature of the tool
 - 2 Update Qt library used to the actual last version
 - 3 Refactor the code
    - a. Design architecture and workflow in UML diagram to represent how it have to be
    - b. splitting correctly the code between view/controller/model part
    - c. clean unused code and libraries/ hunt for some code duplication
    - d. adapt code to pep8

Next feature in mind : 
 - list all caches and dependancies in some json files to display it in the UI and apply action on it
 - improve the view for space used on the hard disk
 - improve the preview feature on the render and flipbook tab
 - render or add to the queue render any version
 - improve the configuration file and test it on different project
 - make a .exe and find a correct way to release it to artists
 - check for possibility to use JS for some more nodal view
 - propose different view for an asset and all its step/substep

Below few picture and a use case of this tool for a video mapping project. In this case the library is more organized as a project library. 
  Library View 
  ![Capture d'écran 2025-03-11 132228](https://github.com/user-attachments/assets/4e85886a-1958-4e25-80d8-c5660b0cdc5c)

  Asset View
  ![Capture d'écran 2025-03-11 132433](https://github.com/user-attachments/assets/17c97eed-d06c-4331-97d0-a4cbbd9388d7)
  ![Capture d'écran 2025-03-11 134220](https://github.com/user-attachments/assets/d016c994-570f-4d8f-9490-3506acf1a7f8)
  ![Capture d'écran 2025-03-11 134028](https://github.com/user-attachments/assets/b6902bfc-6261-43fc-b6d3-50a5930c6f88)

  Use Case for a video mapping : 
  ![Capture d'écran 2025-03-11 133515](https://github.com/user-attachments/assets/b6a203fd-c9bf-478a-8b8e-268d3e652e2b)

  Different project configuration possible
![Capture d'écran 2025-03-11 134924](https://github.com/user-attachments/assets/e5636e70-eda4-4750-a9db-fb093316879c)

