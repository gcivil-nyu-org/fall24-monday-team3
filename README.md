# fall24-monday-team3 Sreeharsh 

<H1> High Level Context Diagram <H1>
<img width="506" alt="Screenshot 2024-09-30 at 11 32 22 AM" src="https://github.com/user-attachments/assets/e8d9f9e7-ad0b-48ce-804e-28b1d39c0274">

<H1>User Personas</H1>


  <h2>Epics</h2>
  <p> There are 2 epics in the project</p>
  <li> Users</li>
  <li> Moderators</li>
  <h3> Users</h3>
  <p>In the application, users range from various backgrounds in real life such as first time renters who are interested in renting an entire apartment or sharing an apartment with other roommates or just interested in knowing more about the rental market in various neighborhoods in NYC. Users persona also encompasses the activities of the experienced Real Estate Investors and Brokers, who are interested in observing long term and short term trends in rental prices in the neighborhoods, in relation to the external circumstances and take informed decisions accordingly. All users, irrespective of their backgrounds, are treated as the same kind of entity. Users can estimate the fair range of rental prices for a property, given the parameters (Ex: area of the property, type of property, neighborhood etc.) using our ML model. Users also can post the property vacancies, partial vacancies and share the rent of their current property and discuss, thus resulting in increased transparency of the market.</p>
  <h3> Moderators</h3>
  <p> Moderators are managing entities or admins of the application, who authorize the users when they are registering them for the first time and moderate the content by checking the alignment with the purpose of thread. Moderators are responsible for collecting vacancies posted by users from the categories and threads of the application and perform efficient data analysis to give better understanding of the current market situation. Moderators also have access to voluntarily improve the efficiency of the price estimation module, by supplying additional datapoints found from anecdotes or other sources.
  </p>

  <h2>Account Registration and Management - User</h2>
    <p>Users can create accounts on the website using their email and password. Email addresses will be verified and a confirmation email will be sent post successful registration. Users can login into the website using their email and password. The user can reset the password and edit the profile information. They can deactivate their accounts and remove their information from the website.</p>


  <ul>
        <li>As a user, I want to be able to create an account using an email address and password.</li>
        <li>As a user, I want to be able to login into my account using my email address and password.</li>
        <li>As a user, I want to be able to reset my password in case I forget it using my email address.</li>
        <li>As a user, I want to be able to view and edit and update my profile information.</li>
        <li>As a user, I want to be able to deactivate my account so that my information no longer exists in the system.</li>
    </ul>

  <h2>Rent Estimation - User</h2>
    <p>The Rent Estimation tool enables the user to find rental prices in different neighborhoods in NYC based on apartment features and amenities. Potential renters or landlords can save their preferences to their account, which will appear on their dashboard, modify and add/remove any preferences. They can also see the price change in apartments over the years which will help them understand the price trends in different neighborhoods and make informed decisions about the rental pricing.</p>


  <ul>
        <li>As a user, I want to input details of an apartment (location, size, amenities, etc.), so that I can get an accurate rent estimate for the property.</li>
        <li>As a user, I want to compare rent prices between different neighborhoods, so that I can evaluate which area offers better value based on my budget and preferences.</li>
        <li>As a user, I want to search for rent estimates in a specific neighborhood, so that I can get detailed information on typical rental prices in that area.</li>
        <li>As a user, I want to filter apartments or neighborhoods by my budget, apartment size, or other preferences (e.g., pet-friendly, near parks, etc.), so that I can quickly find rental options that match my criteria.</li>
        <li>As a user, I want to see historical pricing trends for specific neighborhoods, so that I can understand how rental prices have changed over time and make better decisions for the future.</li>
    </ul>

  <h2>Forum Posting - Vacancies - User</h2>
    <p>The vacancy forum allows users(landlords) to post rental apartment vacancies. The user enters a set of required details, such as the location, rent price, lease period, number of bedrooms, size of the apartment, electronic appliances included, for eg-washing machine, microwave, along with images or videos of the apartment. They can edit the details after posting a listing. Users(renters) can search for apartments of their preference by using filters on neighborhood, amenities and size of the apartment. The user can save any apartments they like, which will appear on their profile dashboard.</p>


  <ul>
        <li>As a user(landlord), I want to create a new rental listing by providing required information (price, location, bedrooms, size, lease period, appliances), so that potential renters can see my available apartments.</li>
        <li>As a user(landlord), I want to edit my existing rental listings, so that I can update information such as price changes or new amenities.</li>
        <li>As a user(renter), I want to view all posted rental listings in the forum, so that I can find available apartments that meet my criteria.</li>
        <li>As a user, I want to filter and search for rental listings based on criteria like price, location, number of bedrooms, and included amenities, so that I can quickly find apartments that match my needs.</li>
        <li>As a user (renter), I want to save or like apartment listings, so that I can easily access them later from my personal dashboard.</li>
    </ul>

  <h2>Forum Posting Rental Prices - User</h2>
    <p>The Forum Posting Rental Prices feature enables users to easily create and manage rental price listings by providing key details like location, price, and type of rental. Once posted, users can manage their listings, including editing, deleting, while following posting guidelines to maintain consistency. Additionally, users receive feedback and notifications on their post status, helping them stay updated on their posts' activity.</p>


  <ul>
        <li>As a user, I want to be able to post rental prices on the forum, so that I can share and find accurate rental information.</li>
        <li>As a user, I want to be able to post rental prices and also attach my property details.</li>
        <li>As a user, I want to manage my rental price posts so that I can keep them up to date and relevant.</li>
        <li>As a user, I want to receive status on my rental price post so that I know my post is posted successfully and being viewed.</li>
        <li>As a user, I want to be guided on how to properly post rental prices to maintain consistency and accuracy.</li>
    </ul>

  <h2>Forum Posting for Roommates and Partial Vacancies - User</h2>
    <p>The Forum Posting for Roommates and Partial Vacancies feature allows users to create detailed posts to find roommates or share partial rental vacancies by providing information like rent per room, location, and roommate preferences. Users can manage their posts by editing, updating, or marking them as filled, ensuring the listings remain relevant. Clear posting guidelines and validation rules help ensure all posts are complete and accurate. Additionally, users receive confirmation and status updates on their posts, keeping them informed about activity or the need for updates.</p>


  <ul>
        <li>As a user, I want to post information about available rooms or partial vacancies in a rental so that I can find potential roommates.</li>
        <li>As a user, I want to be able to post about available rooms or partial vacancies and also attach my property details, and ideal roommate roommate types.</li>
        <li>As a user, I want to be able to manage my roommate or partial vacancy posts so that I can keep them up to date and relevant.</li>
        <li>As a user, I want to receive status on my partial vacancies post so that I know my post is posted successfully and being viewed.</li>
        <li>As a user, I want to be guided on how to properly post roommate or vacancy information, ensuring consistency and quality across posts.</li>
    </ul>

  <h2>Forum Posts Interaction - User</h2>
    <p>The Forum Posts Interaction feature allows users to engage with forum posts by commenting, reacting with predefined emojis or icons, and participating in discussions through threaded replies. Users can edit or delete their comments and receive notifications when others comment on their posts or reply to their comments, keeping them informed and engaged. Additionally, users can report inappropriate comments or reactions to maintain a respectful and well-moderated environment, ensuring a safe space for interaction.</p>


  <ul>
        <li>As a user, I want to comment on forum posts so that I can engage in discussions or ask questions.</li>
        <li>As a user, I want to react to forum posts so that I can quickly express my opinion without leaving a comment by leaving an emoji.</li>
        <li>As a user, I want to receive notifications about new comments on my posts or replies to my comments so that I stay informed about ongoing discussions.</li>
        <li>As a user, I want to reply to comments on my post too.</li>
        <li>As a user, I want to report inappropriate comments or reactions so that the forum remains respectful and well-moderated.</li>
    </ul>

  <h2>Direct Messaging Other Users - User</h2>
    <p>The Direct Messaging Other Users feature allows users to privately communicate with others by sending and receiving direct messages within the forum. Users can initiate conversations from profiles or posts, manage their messages through an inbox-like interface, and control their privacy by setting who can contact them or blocking unwanted users. Additionally, users receive notifications for new messages via alerts, keeping them informed of incoming communications and replies.</p>


  <ul>
        <li>As a user, I want to send direct messages to other users so that I can have private conversations outside the public forum.</li>
        <li>As a user, I want to receive and manage (delete, or pin on top) direct messages so that I can easily organize my private conversations.</li>
        <li>As a user, I want control over who can message me (blocking) so that I can protect my privacy and avoid unwanted contact.</li>
        <li>As a user, I want to receive notifications for new direct messages so that I stay informed about incoming communications.</li>
    </ul>

   <h2>Moderator</h2>

  <h2>Content Moderation - Moderator</h2>
    <p>Moderators are responsible for maintaining the quality and safety of the platform's content and user interactions. They review and manage posts across various sections, including rental listings, roommate requests, and forum discussions. Moderators handle user reports, enforce community guidelines, and ensure the accuracy of rental data. They also support the AI model training process and mediate user conflicts when necessary.</p>

  <ul>
        <li>As a moderator, I want to review and manage forum posts, rental listings, and user-generated content to ensure compliance with platform guidelines.</li>
        <li>As a moderator, I want to investigate and respond to user reports of inappropriate content or behavior to maintain a safe environment.</li>
        <li>As a moderator, I want to enforce posting guidelines for rental prices, roommate requests, and other forum activities to maintain consistency and quality.</li>
        <li>As a moderator, I want to collect and validate rental data from apartment listings to ensure accuracy for analysis and AI model training.</li>
        <li>As a moderator, I want to mediate disputes between users when necessary, especially in roommate or rental-related discussions.</li>
    </ul>

   <h2>User Authentication - Moderator</h2>
    <p>Moderators oversee the user authentication process to ensure the security and integrity of the platform. They monitor account creations, verify email confirmations, and manage password resets. Moderators can review user profiles when necessary and handle account deactivation requests. They also monitor for unusual login patterns, potential security breaches, or bot activities to maintain the overall integrity of the authentication system.</p>


  <ul>
        <li>As a moderator, I want to monitor new account registrations to identify any suspicious patterns, potential abuse, or bot activities.</li>
        <li>As a moderator, I want to oversee the email verification process to ensure it functions correctly and address any issues that arise.</li>
        <li>As a moderator, I want to supervise password reset requests to maintain account security and assist users who encounter problems.</li>
        <li>As a moderator, I want to process and verify account deactivation requests to ensure user data is appropriately handled and removed.</li>
        <li>As a moderator, I want to review user profile information and behavior patterns when necessary to detect and prevent bot accounts or automated activities.</li>
    </ul>

  <h2>Collect Data - Moderator</h2>
    <p>The Collecting Rental Data of Apartment Listings feature allows moderators to extract relevant rental information, such as price, location, and rental type, from forum posts for data analysis. Moderators can manage the collected data (i.e. deleting or modifying entries) for further analysis, while also reviewing and validating the data for completeness and accuracy, ensuring reliable insights.</p>


  <ul>
        <li>As a moderator, I want to collect rental data from apartment listings in the forum so that I can analyze trends and pricing.</li>
        <li>As a moderator, I want to organize and export the collected rental data so that I can use it for reports and analysis.</li>
        <li>As a moderator, I want to review the rental data for accuracy and completeness so that the analysis is reliable.</li>
    </ul>

  <h2>Summary from Vacancy and Rent discussion Train AI model - Moderator</h2>
    <p>The moderator focuses on training a machine learning model using NYC rental data to provide accurate price predictions for apartments. The model will analyze various features, such as location, size, amenities, and historical pricing data. They will oversee the training process, ensuring the model is continually improved with the latest data to enhance prediction accuracy.</p>

  <ul>
        <li>As a user(moderator), I want to gather historical rental data from NYC, so that I can use it to train the machine learning model for accurate price predictions.</li>
        <li>As a user(moderator), I want to train the machine learning model using the gathered rental data, so that it can learn to predict apartment prices based on various features.</li>
        <li>As a user(moderator), I want to evaluate the performance of the trained machine learning model, so that I can determine its accuracy and make necessary adjustments.</li>
        <li>As a user(moderator), I want to update the machine learning model with new rental data, so that the predictions remain accurate and reflect current market trends.</li>
        <li>As a user (renter), I want to receive real-time rent price predictions when searching for apartments, so that I can make informed decisions based on the estimated market value.</li>
    </ul>
