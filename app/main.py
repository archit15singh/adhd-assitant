from neo4j import GraphDatabase
import os

# Get connection details from environment variables
uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")

# Create Neo4j driver
driver = GraphDatabase.driver(uri, auth=(user, password))


def create_data():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

        # Step 1: Create User
        session.run(
            """
        CREATE (u:User {userId: 'user4', name: 'Alex Johnson', email: 'alex.johnson@developer.com', totalProgress: 30, accountCreatedOn: '2023-01-01'});
        """
        )

        # Step 2: Create Goals
        session.run(
            """
        CREATE (g1:Goal {goalId: 'goal1', title: 'Research FAANG Companies', description: 'Study company cultures, job roles, and requirements for Meta, Amazon, Apple, Netflix, Google', 
                         startDate: '2023-01-05', deadline: '2023-02-28', estimatedCompletion: '2023-02-27', currentProgress: 100, status: 'Completed'}),
               (g2:Goal {goalId: 'goal2', title: 'Tailor Resume for Each FAANG Company', description: 'Update and tailor resume for each FAANG company application', 
                         startDate: '2023-03-01', deadline: '2023-03-31', estimatedCompletion: '2023-03-28', currentProgress: 90, status: 'In Progress'}),
               (g3:Goal {goalId: 'goal3', title: 'Apply to FAANG Jobs', description: 'Submit job applications to FAANG companies', 
                         startDate: '2023-04-01', deadline: '2023-06-30', estimatedCompletion: '2023-06-29', currentProgress: 80, status: 'In Progress'}),
               (g4:Goal {goalId: 'goal4', title: 'Prepare for Coding Interviews', description: 'Practice coding problems and algorithms for FAANG coding interviews', 
                         startDate: '2023-07-01', deadline: '2023-09-30', estimatedCompletion: '2023-09-28', currentProgress: 70, status: 'In Progress'});
        """
        )

        # Step 3: Create SubGoals
        session.run(
            """
        CREATE (sg1:SubGoal {subGoalId: 'subgoal1', title: 'Research Meta Software Engineering Roles', description: 'Study job descriptions and roles at Meta', 
                            startDate: '2023-01-05', deadline: '2023-01-15', estimatedCompletion: '2023-01-14', progressPercentage: 100, status: 'Completed'}),
               (sg2:SubGoal {subGoalId: 'subgoal2', title: 'Tailor Resume for Meta', description: 'Update resume to match Meta job requirements', 
                            startDate: '2023-03-01', deadline: '2023-03-10', estimatedCompletion: '2023-03-09', progressPercentage: 90, status: 'In Progress'}),
               (sg3:SubGoal {subGoalId: 'subgoal3', title: 'Submit Application to Meta', description: 'Submit the job application to Meta', 
                            startDate: '2023-04-01', deadline: '2023-04-05', estimatedCompletion: '2023-04-04', progressPercentage: 80, status: 'In Progress'});
        """
        )

        # Step 4: Create Reminders
        session.run(
            """
        CREATE (r1:Reminder {reminderId: 'reminder1', title: 'Follow up with Meta Recruiter', reminderDueDate: '2023-04-15', message: 'Send follow-up email to Meta recruiter'}),
               (r2:Reminder {reminderId: 'reminder2', title: 'Submit Resume for Amazon', reminderDueDate: '2023-05-10', message: 'Submit resume for Amazon Software Engineer role'});
        """
        )

        # Step 5: Create Work Sessions
        session.run(
            """
        CREATE (ws1:WorkSession {workSessionId: 'worksession1', startTime: '2023-01-10T14:00', endTime: '2023-01-10T16:00', sessionDurationHours: 2, 
                                 description: 'Studied Meta job descriptions and requirements'}),
               (ws2:WorkSession {workSessionId: 'worksession2', startTime: '2023-03-05T10:00', endTime: '2023-03-05T12:00', sessionDurationHours: 2, 
                                 description: 'Updated resume to match Meta’s job requirements'});
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
        
        // Userto goals relationships
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
