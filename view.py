from tabulate import tabulate

class StudioView:
    
    @staticmethod
    def show_main_menu():
        print("\n" + "="*45)
        print("🏋️  STUDIO MANAGEMENT SYSTEM - MAIN 🏋️")
        print("="*45)
        print("1. Manage Members 👥")
        print("2. Manage Trainers 🏋️‍♂️")
        print("3. Manage Workout Sessions 📅")
        print("4. Chat with AI Assistant 🤖")
        print("5. Exit System")
        return input("\nPlease select an option (1-5): ")

    @staticmethod
    def show_members_menu():
        print("\n--- 👥 Members Menu ---")
        print("1. Add New Member")
        print("2. Show All Members")
        print("3. Renew Membership")
        print("4. Change Status (Active/Deactive)")
        print("5. Delete Member")
        print("6. Back to Main Menu")
        return input("Select option (1-6): ")

    @staticmethod
    def show_trainers_menu():
        print("\n--- 🏋️‍♂️ Trainers Menu ---")
        print("1. Add New Trainer")
        print("2. Show All Trainers")
        print("3. Back to Main Menu")
        return input("Select option (1-3): ")

    @staticmethod
    def show_sessions_menu():
        print("\n--- 📅 Sessions Menu ---")
        print("1. Create New Session")
        print("2. Enroll Member to Session")
        print("3. Show All Sessions & Enrollments")
        print("4. Back to Main Menu")
        return input("Select option (1-4): ")

    # =======================
    # פונקציות קלט (Inputs)
    # =======================
    @staticmethod
    def _get_base_person_input():
        id_num = input("Enter ID (9 characters): ")
        name = input("Enter Full Name: ")
        phone = input("Enter Phone (min 9 characters): ")
        return id_num, name, phone

    
    @staticmethod
    def get_member_input():
        print("\n[Adding New Member]")
        id_num, name, phone = StudioView._get_base_person_input()
        try:
            balance = int(input("Enter initial entries (e.g. 10/20/30): "))
        except ValueError:
            balance = 0
        return id_num, name, phone, balance  
    

    @staticmethod
    def get_trainer_input():
        print("\n[Adding New Trainer]")
        id_num, name, phone = StudioView._get_base_person_input()
        specialty = input("Enter Specialty (e.g., Yoga, Weights): ")
        rank = input("Enter Rank (e.g., Junior, Senior): ")
        return id_num, name, phone, specialty, rank

    @staticmethod
    def get_renewal_input():
        print("\n[Renew Membership - Add Entries]")
        id_num = input("Enter Member ID: ")
        try:
            entries = int(input("Enter number of entries to add (e.g., 10): "))
        except ValueError:
            entries = 0
        return id_num, entries


    @staticmethod
    def get_status_change_input():
        """ קליטת בחירה לשינוי סטטוס """
        print("\n[Change Member Status]")
        id_num = input("Enter Member ID: ")
        print("1. Set to ACTIVE")
        print("2. Set to DEACTIVE")
        choice = input("Select status (1/2): ")
        return id_num, choice

    @staticmethod
    def get_session_input():
        print("\n[Create Session]")
        session_id = input("Enter Session ID: ")
        name = input("Enter Session Name (e.g. Pilates): ")
        try:
            capacity = int(input("Enter Max Capacity: "))
        except ValueError:
            capacity = 10
        trainer_id = input("Enter Trainer ID for this session: ")
        return session_id, name, capacity, trainer_id

    @staticmethod
    def get_enrollment_input():
        print("\n[Enroll Member]")
        session_id = input("Enter Session ID: ")
        member_id = input("Enter Member ID to enroll: ")
        return session_id, member_id

    @staticmethod
    def get_delete_id_input():
        print("\n[Delete Member]")
        id_num = input("Enter Member ID to delete: ")
        return id_num

    # ==========================================
    # פונקציות הדפסה (Outputs)
    # ==========================================
    @staticmethod
    def show_members_table(members_data):
        if not members_data:
            print("\n❌ No members found.")
            return
        headers = ["ID Number", "Name", "Phone", "Type", "Balance", "Status"]
        print("\n" + tabulate(members_data, headers=headers, tablefmt="fancy_grid"))

    @staticmethod
    def show_trainers_table(trainers_data):
        if not trainers_data:
            print("\n❌ No trainers found.")
            return
        headers = ["ID Number", "Name", "Phone", "Specialty", "Rank"]
        print("\n" + tabulate(trainers_data, headers=headers, tablefmt="fancy_grid"))

    @staticmethod
    def show_sessions(session_objects):
        if not session_objects:
            print("\n❌ No sessions found.")
            return
        print("\n" + "="*45 + "\n🏋️  ALL WORKOUT SESSIONS 🏋️\n" + "="*45)
        for session in session_objects:
            trainer_name = session.trainer._name if session.trainer else "No Trainer"
            print(f"🔹 Session: [{session.session_id}] {session.name}")
            print(f"   Trainer: {trainer_name} | Capacity: {len(session.members)}/{session.max_capacity}")
            if session.members:
                print("   Enrolled Members:")
                for m in session.members:
                    print(f"      - {m._name} (ID: {m.id_num})")
            else:
                print("   Enrolled Members: None yet.")
            print("-" * 45)

    @staticmethod
    def show_message(msg):
        print(f"\n>>> {msg}")

    # ==================
    # פונקציות צ'אט AI
    # ==================
    @staticmethod
    def get_ai_chat_input():
        return input("\n👤 You: ")

    @staticmethod
    def show_ai_thinking():
        print("🤖 AI: Thinking...", end="\r")

    @staticmethod
    def show_ai_response(response_text):
        print(" " * 20, end="\r") 
        print(f"🤖 AI: {response_text}")





