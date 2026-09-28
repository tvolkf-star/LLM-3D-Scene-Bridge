# Direct Modeling in Autodesk 3ds Max via ChatGPT and an Executable Representation of a 3D Scene

[Русская версия](RESEARCH_RU.md) · [Repository overview](README.md)

## 1. Background

Modern language models can work confidently with program code, analyze images, and solve tasks that require sequential decision-making. At the same time, professional 3D modeling systems already provide full programmatic interfaces for scene control.

This raises a fairly simple question: **is a specialized AI system for modeling necessary, or is it enough to give a general-purpose language model a direct control channel to an existing professional tool?**

The experiment used **Autodesk 3ds Max 2024** as the working environment and **ChatGPT GPT-5.6 Sol in Instant mode** as the controlling model.

A key condition was to preserve the standard modeling environment. The experiment did not involve creating a separate 3D editor, a specialized generative model, or replacing geometry with an image. The result had to be ordinary native 3ds Max objects that remained available for further editing with the standard tools of the application.

Interaction also had to take place through the ordinary ChatGPT user interface. The user describes a task in natural language; the subsequent technical cycle of transmitting and executing commands takes place without manually copying generated code into 3ds Max.

In other words, the research question was not:

**“Can AI write a script for 3ds Max?”**

That question is no longer particularly interesting.

The question was:

**“Can a general-purpose language model work directly as a modeler inside a professional 3D environment?”**

---

## 2. Subject of the experiment

For the experiment, ChatGPT proposed the architecture of a bidirectional software bridge between its interface and a locally running Autodesk 3ds Max.

Data transfer was organized through a synchronized Google Drive directory:

**ChatGPT → Google Drive → local synchronization → Python/pymxs → Autodesk 3ds Max**

The return channel was:

**3ds Max → scene state + execution result + viewport image → Google Drive → ChatGPT**

Google Drive does not participate in modeling and contains no special modeling logic. It acts as a transport layer between the remote language-model interface and the local professional application.

The bridge itself is deliberately minimal.

It does not model on behalf of ChatGPT and contains no library of predefined high-level commands such as “create a house”, “create a chair”, or “build a facade”. Its task is to provide access to Python/pymxs, execute the operation formed by the model, and return the actual state of the environment.

Thus, **the intelligence of the system remains on the general-purpose LLM side, while the geometry remains on the 3ds Max side.**

The bridge connects them.

---

## 3. Course of the experiment

After the bridge was launched, the user assigned tasks directly in the ChatGPT window using ordinary text.

ChatGPT independently formed the program for constructing an object; transmitted it through the bridge; initiated execution in 3ds Max; created native scene objects; received information about the result; analyzed errors; and changed its construction method in subsequent iterations.

The first experiments used elementary geometry, after which the complexity of the task was increased.

From a textual architectural description, ChatGPT constructed a shopping-center scene consisting of **69 separate native 3ds Max objects**. The geometry was created directly inside the professional environment and remained available for standard editing.

The next experiment focused on object modeling.

An IKEA FROSTA stool was used as the initial constructive reference. During modeling, ChatGPT proposed its own geometry for the bent supports — thinner and more plastic than the original reference. The resulting form was evaluated by the architect and deliberately retained as an independent design variant.

This became **GPT Stool No. 1**.

The experiment was important not only because of the result, but because of the process. After professional correction of the construction method, ChatGPT moved from direct polygonal construction to a method appropriate to this task:

**SplineShape → rectangular section → Editable Poly → relative instance transformations.**

In other words, the collaborative work did not manually correct the model itself; it corrected **the modeling method used by the language model**.

ChatGPT then independently reproduced the object using 3ds Max.

---

## 4. Transfer of a professional modeling method

The next stage tested whether a language model could learn not a specific object to copy, but the logic of a professional modeling method and apply it to a new task.

The architect demonstrated a principle used in professional practice for constructing repeated spatial systems through paths, animation, and Snapshot in Autodesk 3ds Max. A single source profile or object is given a rule that changes its position, shape, scale, section, or other parameters; a sequence of its states is materialized as geometry; the result is then cleaned of construction objects and consolidated into ordinary editable scene geometry.

The examples were not supplied as objects to reproduce. They demonstrated the logic and the range of applications of the method: small architectural forms, lamellar systems, walls, canopies, and facade elements.

After the explanation, ChatGPT received a new task and independently applied the learned principle while modeling an elongated small architectural form with an integrated seat and canopy.

The first iterations revealed errors in form and ergonomics. Professional feedback did not consist of manually positioning individual elements; it addressed the construction logic itself — the profile, the character of transitions, lamella section, and organization of the modeling workflow. Subsequent iterations produced a substantial change in the result.

The resulting form was then duplicated, rotated, and tested as a spatial module on a scene plane. The module retained compositional integrity and remained suitable for further work in the standard 3ds Max environment.

Thus, the experiment demonstrated transfer from a human professional to a language model of **not only an example object, but a professional modeling method**, which the model then applied to a new geometric task.

---

## 5. Additional investigation: scene reproducibility

The result raised another question.

If ChatGPT can describe its own scene-construction process using Python/pymxs, must the result of modeling necessarily exist only as a traditional scene file?

ChatGPT converted the created object into an autonomous Python script containing the procedure for constructing it.

The script contained the seat geometry, the geometry and trajectory of the support, section parameters, dimensions, spatial placement of elements, copying, and transformations.

Thus, the file preserved more than the final set of geometric data.

**It preserved the method by which the scene was produced.**

---

## 6. Course of the additional investigation

A separate instance of Autodesk 3ds Max was launched to test reproducibility.

It:

- was not connected to the developed bridge;
- did not contain the original scene;
- had not participated in the modeling process.

Only the autonomous Python/pymxs script for **GPT Stool No. 1** was passed to it.

After execution, the object was rebuilt in the independent environment.

Its geometric structure, dimensions, element positions, and constructive organization were reproduced. The result was again ordinary editable Autodesk 3ds Max objects.

The original scene therefore ceased to be a necessary carrier of the object.

To restore it, an **executable description of the construction procedure** was sufficient.

---

## 7. Evidence

The result is reproducible and can be presented directly, without requiring the reader to trust the description of the experiment.

The demonstration materials include:

- source code of the ChatGPT ↔ 3ds Max software bridge;
- data-exchange scheme;
- commands formed by ChatGPT;
- machine-readable scene-state snapshots;
- viewport images obtained during modeling;
- the native 3ds Max scene;
- the autonomous Python/pymxs script for GPT Stool No. 1;
- the result of executing that script in an independent instance of 3ds Max.

The key reproducibility test is therefore extremely simple:

**empty 3ds Max + one Python file → restored editable scene.**

The bridge itself is also reproducible: its source code requires neither a specialized machine-learning model nor a separate generative 3D engine.

---

## 8. Conclusions

The experiment showed that a general-purpose language model can be incorporated directly into a professional 3D-modeling loop.

In the implemented system, **ChatGPT does not merely advise the modeler or output code for the user to execute manually. It performs the modeling role itself**: it receives a task in natural language, forms a construction method, controls 3ds Max, and receives the result of its work back.

At the same time, 3ds Max remains 3ds Max.

No intermediate “AI geometry” is created that must later be converted into a professional format. The result is immediately composed of standard objects in a professional DCC system.

The subsequent experiment also tested transfer of a professional modeling method: the architect explained the logic of a working method rather than supplying finished geometry to copy. After several iterations and professional feedback, ChatGPT applied the principle to a new task and created an independent spatial form.

But the most interesting result emerged as a secondary consequence of the original experiment.

The created scene proved representable as **executable source code**.

Such a representation has properties of both a traditional scene and a program: it stores geometric construction, parameters, and relationships between objects; it can reconstruct the scene by itself; and it remains a textual programmatic description of how that scene is built.

In our experiment it has already demonstrated the essential property of an exchange representation:

**the same scene was reproduced in an independent environment from the transferred representation.**

The carrier is Python — a language suitable both for machine execution and for programmatic analysis and transformation, including by systems that work with source code.

This changes the framing of the original problem in an interesting way.

We began by trying to give ChatGPT hands inside 3ds Max.

The result was a working bidirectional interface between a general-purpose LLM and a professional DCC system; independent creation of native geometry by the model; transfer of a professional modeling method from an architect to the language model; and independent reconstruction of the created scene from an executable description.

**And then we found that what can be transferred is no longer limited to the model’s commands.**

**The scene itself can be transferred as a program.**
