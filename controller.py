from model import StudioModel
from view import StudioView
from entities import Member, Trainer, WorkoutSession
from ollama import Client

class MainController:
    def __init__(self):
        self.model = StudioModel()
        self.view = StudioView()
        self.ai_client = Client(host='http://localhost:11435')

    # ======================
    # ניהול לולאות ראשיות 
    # ======================
    def run(self):
        self.view.show_message("Welcome to the Studio Management System!")
        while True:
            choice = self.view.show_main_menu()
            try:
                if choice == '1':
                    self._manage_members_loop()
                elif choice == '2':
                    self._manage_trainers_loop()
                elif choice == '3':
                    self._manage_sessions_loop()
                elif choice == '4':
                    self._chat_with_ai()
                elif choice == '5':
                    self.view.show_message("Exiting system. Goodbye! 👋")
                    break 
                else:
                    self.view.show_message("Invalid choice. Please try again.")
            except Exception as e:
                self.view.show_message(f"System Error: {e}")

    def _manage_members_loop(self):
        while True:
            choice = self.view.show_members_menu()
            try:
                if choice == '1':
                    self._add_member()
                elif choice == '2':
                    self._show_members()
                elif choice == '3':
                    self._renew_membership()
                elif choice == '4':
                    self._change_member_status() 
                elif choice == '5':
                    self._delete_member()
                elif choice == '6':
                    break 
                else:
                    self.view.show_message("Invalid choice.")
            except ValueError as e:
                self.view.show_message(f"Validation Error: {e}")

    def _manage_trainers_loop(self):
        while True:
            choice = self.view.show_trainers_menu()
            if choice == '1':
                self._add_trainer()
            elif choice == '2':
                self._show_trainers()
            elif choice == '3':
                break
            else:
                self.view.show_message("Invalid choice.")

    def _manage_sessions_loop(self):
        while True:
            choice = self.view.show_sessions_menu()
            if choice == '1':
                self._create_session()
            elif choice == '2':
                self._enroll_member()
            elif choice == '3':
                self._show_sessions()
            elif choice == '4':
                break
            else:
                self.view.show_message("Invalid choice.")

    # ===============
    # פעולות מנויים 
    # ===============

    
    def _add_member(self):
        id_num, name, phone, initial_balance = self.view.get_member_input()
        new_member = Member(id_num, name, phone, member_type="Punch Card", balance=initial_balance)
        self.model.save_person(new_member)
        self.view.show_message(f"Member '{name}' added successfully with {initial_balance} entries!")
    

    def _show_members(self):
        members_data = self.model.get_all_members()
        self.view.show_members_table(members_data)

    def _renew_membership(self):
        id_num, amount = self.view.get_renewal_input()
        member_data = self.model.read_member(id_num)
        if not member_data:
            self.view.show_message("❌ Member not found.")
            return
            
        member_obj = Member(member_data[0], member_data[1], member_data[2], member_data[3], member_data[4], member_data[5])
        member_obj.renew_membership(amount)
        self.model.save_person(member_obj)
        self.view.show_message(f"Success! {member_obj._name}'s membership renewed. Balance: {member_obj.balance}")

    def _change_member_status(self):
        id_num, choice = self.view.get_status_change_input()
        member_data = self.model.read_member(id_num)
        if not member_data:
            self.view.show_message("❌ Member not found.")
            return
            
        member_obj = Member(member_data[0], member_data[1], member_data[2], member_data[3], member_data[4], member_data[5])
        
        if choice == '1':
            member_obj.status = "Active"
            self.view.show_message(f"{member_obj._name} is now ACTIVE.")
        elif choice == '2':
            member_obj.deactivate() 
            self.view.show_message(f"{member_obj._name} is now DEACTIVE.")
        else:
            self.view.show_message("Invalid option.")
            return
            
        self.model.save_person(member_obj)

    def _delete_member(self):
        id_num = self.view.get_delete_id_input()
        success = self.model.delete_member(id_num)
        
        if success:
            self.view.show_message(f"✅ Member with ID '{id_num}' was deleted.")
        else:
            self.view.show_message(f"❌ Member with ID '{id_num}' not found.")

    # ========================
    # פעולות מאמנים ואימונים 
    # ========================

    def _add_trainer(self):
        id_num, name, phone, specialty, rank = self.view.get_trainer_input()
        new_trainer = Trainer(id_num, name, phone, specialty, rank)
        self.model.save_person(new_trainer)
        self.view.show_message(f"Trainer '{name}' added successfully!")

    def _show_trainers(self):
        trainers_data = self.model.get_all_trainers()
        self.view.show_trainers_table(trainers_data)

    def _create_session(self):
        session_id, name, capacity, trainer_id = self.view.get_session_input()
        trainer_data = self.model.read_trainer(trainer_id)
        if not trainer_data:
            self.view.show_message("❌ Trainer not found! Cannot create session.")
            return
        
        trainer_obj = Trainer(trainer_data[0], trainer_data[1], trainer_data[2], trainer_data[3], trainer_data[4])
        new_session = WorkoutSession(session_id, name, trainer_obj, capacity)
        self.model.save_session(new_session)
        self.view.show_message(f"Session '{name}' created successfully with Trainer {trainer_obj._name}!")

    def _enroll_member(self):
        session_id, member_id = self.view.get_enrollment_input()
        member_data = self.model.read_member(member_id)
        if not member_data:
            self.view.show_message("❌ Member not found.")
            return
            
        member_obj = Member(member_data[0], member_data[1], member_data[2], 
                            member_data[3], member_data[4], member_data[5])
        
        if member_obj.deduct_entry():
            self.model.enroll_member_to_session(session_id, member_id)
            
            self.model.save_person(member_obj)
            
            self.view.show_message(f"✅ Success! {member_obj._name} enrolled to session {session_id}. Entries left: {member_obj.balance}")
        else:
            self.view.show_message(f"❌ Cannot enroll. {member_obj._name} has 0 entries left! Please renew membership.")
    
    
    def _show_sessions(self):
        sessions_data = self.model.get_all_sessions()
        session_objects = []
        for s_data in sessions_data:
            session_id, name, trainer_id, capacity = s_data
            trainer_obj = None
            if trainer_id:
                t_data = self.model.read_trainer(trainer_id)
                if t_data:
                    trainer_obj = Trainer(t_data[0], t_data[1], t_data[2], t_data[3], t_data[4])
            
            session = WorkoutSession(session_id, name, trainer_obj, capacity)
            members_data = self.model.get_members_in_session(session_id)
            for m_data in members_data:
                member_obj = Member(m_data[0], m_data[1], m_data[2], m_data[3], m_data[4], m_data[5])
                session.members.append(member_obj)
                
            session_objects.append(session)
        self.view.show_sessions(session_objects)

    # ===========
    # פעולות AI
    # ===========

    def _chat_with_ai(self):
        self.view.show_message("Entering AI Chat Mode. Type 'exit' to return.")
        while True:
            user_msg = self.view.get_ai_chat_input()
            
            if user_msg.lower() in ['exit', 'quit']:
                self.view.show_message("Exiting AI Chat Mode...")
                break
                
            try:
                studio_data = self.model.get_studio_summary_for_ai()
                full_prompt = f"Studio Data: {studio_data}\nUser Question: {user_msg}"
                
                self.view.show_ai_thinking() 
                
                response = self.ai_client.chat(
                    model='mistral', 
                    messages=[{'role': 'user', 'content': full_prompt}]
                )
                
                self.view.show_ai_response(response['message']['content'])
                
            except Exception as e:
                self.view.show_message(f"❌ Failed to connect to Ollama. Error: {e}")
                break