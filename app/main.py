from neo4j import GraphDatabase
import os
from datetime import datetime, timedelta

# Get connection details from environment variables
uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")

# Create Neo4j driver
driver = GraphDatabase.driver(uri, auth=(user, password))

# Calculate today's, yesterday's, and last week's dates
today = datetime.now().strftime("%Y-%m-%d")
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
last_week = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")


def create_data():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

        # Step 1: Create User
        session.run(
            f"""
        CREATE (u:User {{userId: 'user4', name: 'Alex Johnson', email: 'alex.johnson@developer.com', totalProgress: 30, accountCreatedOn: '{last_week}'}});
        """
        )

        # Step 2: Create Goals
        session.run(
            f"""
        CREATE (g1:Goal {{goalId: 'goal1', title: 'Research FAANG Companies', description: 'Study company cultures, job roles, and requirements for Meta, Amazon, Apple, Netflix, Google', 
                         startDate: '{last_week}', deadline: '{yesterday}', estimatedCompletion: '{yesterday}', currentProgress: 100, status: 'Completed'}}),
               (g2:Goal {{goalId: 'goal2', title: 'Tailor Resume for Each FAANG Company', description: 'Update and tailor resume for each FAANG company application', 
                         startDate: '{last_week}', deadline: '{today}', estimatedCompletion: '{yesterday}', currentProgress: 90, status: 'In Progress'}}),
               (g3:Goal {{goalId: 'goal3', title: 'Apply to FAANG Jobs', description: 'Submit job applications to FAANG companies', 
                         startDate: '{yesterday}', deadline: '{today}', estimatedCompletion: '{yesterday}', currentProgress: 80, status: 'In Progress'}}),
               (g4:Goal {{goalId: 'goal4', title: 'Prepare for Coding Interviews', description: 'Practice coding problems and algorithms for FAANG coding interviews', 
                         startDate: '{today}', deadline: '{today}', estimatedCompletion: '{yesterday}', currentProgress: 70, status: 'In Progress'}});
        """
        )

        # Step 3: Create SubGoals
        session.run(
            f"""
        CREATE (sg1:SubGoal {{subGoalId: 'subgoal1', title: 'Research Meta Software Engineering Roles', description: 'Study job descriptions and roles at Meta', 
                            startDate: '{last_week}', deadline: '{yesterday}', estimatedCompletion: '{yesterday}', progressPercentage: 100, status: 'Completed'}}),
               (sg2:SubGoal {{subGoalId: 'subgoal2', title: 'Tailor Resume for Meta', description: 'Update resume to match Meta job requirements', 
                            startDate: '{yesterday}', deadline: '{today}', estimatedCompletion: '{yesterday}', progressPercentage: 90, status: 'In Progress'}}),
               (sg3:SubGoal {{subGoalId: 'subgoal3', title: 'Submit Application to Meta', description: 'Submit the job application to Meta', 
                            startDate: '{yesterday}', deadline: '{today}', estimatedCompletion: '{yesterday}', progressPercentage: 80, status: 'In Progress'}});
        """
        )

        # Step 4: Create Reminders
        session.run(
            f"""
        CREATE (r1:Reminder {{reminderId: 'reminder1', title: 'Follow up with Meta Recruiter', reminderDueDate: '{yesterday}', message: 'Send follow-up email to Meta recruiter'}}),
               (r2:Reminder {{reminderId: 'reminder2', title: 'Submit Resume for Amazon', reminderDueDate: '{today}', message: 'Submit resume for Amazon Software Engineer role'}});
        """
        )

        # Step 5: Create Work Sessions
        session.run(
            f"""
        CREATE (ws1:WorkSession {{workSessionId: 'worksession1', startTime: '{yesterday}T14:00', endTime: '{yesterday}T16:00', sessionDurationHours: 2, 
                                 description: 'Studied Meta job descriptions and requirements'}}),
               (ws2:WorkSession {{workSessionId: 'worksession2', startTime: '{today}T10:00', endTime: '{today}T12:00', sessionDurationHours: 2, 
                                 description: 'Updated resume to match Meta’s job requirements'}});
        """
        )

        # Step 6: Create Relationships Between User, Goals, SubGoals, Reminders, and Work Sessions
        session.run(
            """
        MATCH (u:User {userId: 'user4'}), 
            (g1:Goal {goalId: 'goal1'}), (g2:Goal {goalId: 'goal2'}),
            (g3:Goal {goalId: 'goal3'}), (g4:Goal {goalId: 'goal4'}),
            (sg1:SubGoal {subGoalId: 'subgoal1'}), (sg2:SubGoal {subGoalId: 'subgoal2'}),
            (sg3:SubGoal {subGoalId: 'subgoal3'}),
            (r1:Reminder {reminderId: 'reminder1'}), (r2:Reminder {reminderId: 'reminder2'}),
            (ws1:WorkSession {workSessionId: 'worksession1'}), (ws2:WorkSession {workSessionId: 'worksession2'})
        
        // User to goals relationships
        CREATE (u)-[:HAS_GOAL]->(g1), (u)-[:HAS_GOAL]->(g2), (u)-[:HAS_GOAL]->(g3), (u)-[:HAS_GOAL]->(g4)

        // Goal to SubGoal relationships
        CREATE (g1)-[:HAS_SUBGOAL]->(sg1), (g2)-[:HAS_SUBGOAL]->(sg2), (g3)-[:HAS_SUBGOAL]->(sg3)

        // Reminder relationships
        CREATE (r1)-[:REMINDER_FOR]->(sg1), (r2)-[:REMINDER_FOR]->(sg2)

        // Work session relationships
        CREATE (ws1)-[:SESSION_FOR]->(sg1), (ws2)-[:SESSION_FOR]->(sg2);
        """
        )


def fetch_data():
    with driver.session() as session:
        result = session.run(
            """
            MATCH (u:User)-[:HAS_GOAL]->(g:Goal) 
            RETURN u.name AS user, g.title AS goal, g.deadline AS deadline
            """
        )
        for record in result:
            print(
                f"User: {record['user']} | Goal: {record['goal']} | Deadline: {record['deadline']}"
            )


if __name__ == "__main__":
    create_data()  # Create the user, goals, sub-goals, reminders, and work sessions
    fetch_data()  # Fetch and print the data
