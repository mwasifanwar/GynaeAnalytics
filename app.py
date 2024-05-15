import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset
@st.cache
def load_data():
    # Load your CSV file or database here
    df = pd.read_csv('Dataset.csv')
    return df

def main():
    st.sidebar.title('Select the Analysis')
    selected_option = st.sidebar.selectbox('Select an option', ('Age and Childbirth History', 'Contraceptive History and Age', 'Hospital Comparison', 'Age vs Origin of Patient', 'Occupation vs. Medical Conditions'))

    # Load the data
    df = load_data()

    if selected_option == 'Age and Childbirth History':
        st.title('Age Distribution of Patients with Respect to Childbirth History (Nulliparous vs. Multiparous)')
        
        # Filter nulliparous and multiparous patients
        filtered_df = df[df['Child_Birth'].isin(['Nulliparous', 'Multiparous'])]

        age_bins = [18, 25, 35, 45, 55]  # Define your age bins
        age_labels = ['18-24', '25-34', '35-44', '45-54']
        filtered_df['Age Group'] = pd.cut(filtered_df['Age'], bins=age_bins, labels=age_labels, right=False)

        age_childbirth_counts = filtered_df.groupby(['Age Group', 'Child_Birth']).size().unstack(fill_value=0)

        info_text = '''
        - Each bar in the chart represents an age group, and within each bar, different segments denote the number of patients with childbirth history within that age group.
        - The x-axis represents the age groups, while the y-axis displays the number of patients.
        - The bars are stacked to show the cumulative count of patients with childbirth history within each age group.
        - Each pie chart in the 2x2 grid represents a specific age group, and the slices within each pie chart represent the percentage distribution of patients age group with certain childbirth history.
        '''
        with st.expander("💡Info"):
            st.write(info_text)
        
        fig, ax = plt.subplots(2, 1, figsize=(10, 20))  # Larger figure size for better readability

        # Bar chart
        age_childbirth_counts.plot(kind='bar', stacked=True, ax=ax[0])
        ax[0].set_xlabel('Age Group')
        ax[0].set_ylabel('Number of Patients')
        ax[0].set_title('Age Distribution of Patients with Respect to Childbirth History (Nulliparous vs. Multiparous)')
        ax[0].legend(title='Childbirth History', loc='upper right')

        for p in ax[0].patches:
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy() 
            ax[0].annotate(f'{height:.0f}', (x + width/2, y + height + 5), ha='center')

        ax[1].pie(age_childbirth_counts.sum(), labels=age_childbirth_counts.sum().index, autopct='%1.1f%%', startangle=90)
        ax[1].set_title('Percentage Distribution by Childbirth History')

        st.pyplot(fig)

    elif selected_option == "Contraceptive History and Age":
        st.title('Age Distribution of Patients with Respect to Contraceptive History (Yes vs. No)')
        
        contraceptive_df = df[df['Contraceptive_History'].isin(['Yes', 'No'])]

        age_bins = [18, 25, 35, 45, 55]  # Define your age bins
        age_labels = ['18-24', '25-34', '35-44', '45-54']
        contraceptive_df['Age Group'] = pd.cut(contraceptive_df['Age'], bins=age_bins, labels=age_labels, right=False)

        age_contraceptive_counts = contraceptive_df.groupby(['Age Group', 'Contraceptive_History']).size().unstack(fill_value=0)

        info_text = '''
        - Each bar in the chart represents an age group, and within each bar, different segments denote the number of patients with contraceptive history within that age group.
        - The x-axis represents the age groups, while the y-axis displays the number of patients.
        - The bars are stacked to show the cumulative count of patients with contraceptive history within each age group.
        - Each pie chart in the 2x2 grid represents a specific age group, and the slices within each pie chart represent the percentage distribution of patients age group taking contraceptive or not.
        '''
        with st.expander("💡Info"):
            st.write(info_text)

        fig, ax = plt.subplots(2, 1, figsize=(10, 20))  # Larger figure size for better readability

        age_contraceptive_counts.plot(kind='bar', stacked=True, ax=ax[0])
        ax[0].set_xlabel('Age Group')
        ax[0].set_ylabel('Number of Patients')
        ax[0].set_title('Age Distribution of Patients with Respect to Contraceptive History (Yes vs. No)')
        ax[0].legend(title='Contraceptive History', loc='upper right')

        for p in ax[0].patches:
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy() 
            ax[0].annotate(f'{height:.0f}', (x + width/2, y + height + 5), ha='center')

        age_contraceptive_counts.sum().plot(kind='pie', autopct='%1.1f%%', ax=ax[1], startangle=90)
        ax[1].set_title('Overall Distribution of Contraceptive History (Yes vs. No)')

        st.pyplot(fig)

    elif selected_option == "Hospital Comparison":
        st.title('Age Distribution of Patients with Respect to Hospital Visits')
        
        hospitals = ['CMH Lahore', 'Allied Hospital Faisalabad', 'DHQ Faisalabad']
        hospital_df = df[df['Hospital'].isin(hospitals)]

        age_bins = [18, 25, 35, 45, 55]  # Define your age bins
        age_labels = ['18-24', '25-34', '35-44', '45-54']
        hospital_df['Age Group'] = pd.cut(hospital_df['Age'], bins=age_bins, labels=age_labels, right=False)

        age_hospital_counts = hospital_df.groupby(['Age Group', 'Hospital']).size().unstack(fill_value=0)
        
        info_text = '''
        - Each bar in the chart represents an age group, and within each bar, different segments denote the number of patients visit to different hospitals within that age group.
        - The x-axis represents the age groups, while the y-axis displays the number of patients.
        - The bars are stacked to show the cumulative count of patients across different hospitals within each age group.
        '''
        with st.expander("💡Info"):
            st.write(info_text)
        
        fig, ax = plt.subplots(figsize=(10, 6))  # Larger figure size for better readability
        age_hospital_counts.plot(kind='bar', stacked=True, ax=ax)
        ax.set_xlabel('Age Group')
        ax.set_ylabel('Number of Patients')
        ax.set_title('Age Distribution of Patients with Respect to Hospital Visits')
        ax.legend(title='Hospital', loc='upper right')
        
        for p in ax.patches:
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy() 
            ax.annotate(f'{height:.0f}', (x + width/2, y + height + 5), ha='center')

        st.pyplot(fig)

        age_hospital_counts = hospital_df.groupby(['Age Group', 'Hospital']).size().unstack(fill_value=0)

        info_text = '''
        - Each pie chart in the 2x2 grid represents a specific age group, and the slices within each pie chart represent the percentage distribution of patients across different hospitals.
        '''
        with st.expander("💡Info"):
            st.write(info_text)

        fig, axs = plt.subplots(3, 1, figsize=(10, 20))

        for i, hospital in enumerate(hospitals):
            hospital_data = age_hospital_counts[hospital]
            axs[i].pie(hospital_data, labels=hospital_data.index, autopct='%1.1f%%', startangle=90)
            axs[i].set_title(f'Age Distribution for {hospital}')
        
        st.pyplot(fig)

    elif selected_option == "Age vs Origin of Patient":

        st.title('Age Distribution of Patients with Respect to Origin City Address')

        origin_cities = ['Jaranwala', 'Khurrianwala', 'Sheikhupura', 'Lahore', 'Pattoki', 'Faisalabad', 'Manawala']

        filtered_df = df[df['Address'].isin(origin_cities)]

        # Create age groups
        age_bins = [18, 25, 35, 45, 55]  # Define your age bins
        age_labels = ['18-24', '25-34', '35-44', '45-54']
        filtered_df['Age Group'] = pd.cut(filtered_df['Age'], bins=age_bins, labels=age_labels, right=False)

        # Count the number of patients in each age group with respect to origin cities
        age_city_counts = filtered_df.groupby(['Age Group', 'Address']).size().unstack(fill_value=0)

        info_text = '''
        - Each bar in the chart represents an age group, and within each bar, different segments denote the number of patients from different origin cities within that age group.
        - The x-axis represents the age groups, while the y-axis displays the number of patients.
        - The bars are stacked to show the cumulative count of patients across different origin cities within each age group.
        '''
        with st.expander("💡Info"):
            st.write(info_text)

        fig, ax = plt.subplots(figsize=(10, 6))  # Larger figure size for better readability
        age_city_counts.plot(kind='bar', stacked=True, ax=ax)
        ax.set_xlabel('Age Group')
        ax.set_ylabel('Number of Patients')
        ax.set_title('Age Distribution of Patients with Respect to Origin City Address')
        ax.legend(title='Origin City', loc='upper right')

        # Adding percentage values on top of each bar
        for p in ax.patches:
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy() 
            ax.annotate(f'{height:.0f}', (x + width/2, y + height + 5), ha='center')

        st.pyplot(fig)

        st.title('Age Distribution of Patients with Respect to Origin City Address')

        # Define the list of origin cities to analyze
        origin_cities = ['Jaranwala', 'Khurrianwala', 'Sheikhupura', 'Lahore', 'Pattoki', 'Faisalabad', 'Manawala']

        # Filter patients based on origin cities
        filtered_df = df[df['Address'].isin(origin_cities)]

        age_bins = [18, 25, 35, 45, 55]  # Define your age bins
        age_labels = ['18-24', '25-34', '35-44', '45-54']
        filtered_df['Age Group'] = pd.cut(filtered_df['Age'], bins=age_bins, labels=age_labels, right=False)

        age_city_counts = filtered_df.groupby(['Age Group', 'Address']).size().unstack(fill_value=0)

        percentage_counts = age_city_counts.div(age_city_counts.sum(axis=1), axis=0) * 100

        info_text = '''
        - Each pie chart in the 2x2 grid represents a specific age group, and the slices within each pie chart represent the percentage distribution of patients across different origin cities within that age group.
        '''
        with st.expander("💡Info"):
            st.write(info_text)

        fig, axs = plt.subplots(2, 2, figsize=(12, 12))  # Create a 2x2 grid for pie charts

        for i, age_group in enumerate(age_labels):
            ax = axs[i // 2, i % 2]
            percentages = percentage_counts.loc[age_group]
            ax.pie(percentages, labels=percentage_counts.columns, autopct='%1.1f%%', startangle=90)
            ax.set_title(f'Age Group: {age_group}')

        st.pyplot(fig)

    elif selected_option == "Occupation vs. Medical Conditions":

        st.title('Medication Usage Patterns Analysis')

        medication_df = df[['Medications', 'Age', 'Occupation', 'Medical_History']]
        # Count the occurrences of each medication
        medication_counts = medication_df['Medications'].value_counts()

        info_text = '''
        - This bar chart visualizes the usage patterns of medications based on their frequency of prescription.
        - Each bar represents a medication, and the height of the bar indicates the number of patients prescribed that medication.
        - The x-axis displays the medications, while the y-axis shows the count of patients.
        - The chart is sorted to display the top 10 most commonly prescribed medications.
        - By examining this chart, one can identify which medications are frequently prescribed within the dataset.
        - For example, if a medication has a taller bar, it signifies that it is prescribed to a larger number of patients.
        '''
        with st.expander("💡Info"):
            st.write(info_text)

        st.subheader('Bar Chart: Top Medications Usage')
        fig, ax = plt.subplots(figsize=(10, 6))
        medication_counts.head(10).plot(kind='bar', ax=ax)
        ax.set_xlabel('Medications')
        ax.set_ylabel('Number of Patients')
        ax.set_title('Top Medications Usage')
        st.pyplot(fig)

        top_medications = medication_counts.head(5).index.tolist()
        filtered_medication_df = medication_df[medication_df['Medications'].isin(top_medications)]

        info_text = '''
            - This visualization explores the relationship between occupation and medical conditions.
            - The heatmap displays the frequency of different medical conditions across various occupations.
            - Each cell in the heatmap represents the count of patients having a specific medical condition within a particular occupation.
            - A higher count in a cell indicates a higher prevalence of that medical condition among individuals with that occupation.
            - The color intensity of each cell represents the count, with darker shades indicating higher counts and lighter shades indicating lower counts.
        '''
        with st.expander("💡Info"):
            st.write(info_text)

        st.subheader('Heatmap: Medications vs. Occupation')
        medication_occ_corr = pd.pivot_table(data=filtered_medication_df, index='Medications', columns='Occupation', aggfunc='size', fill_value=0)
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        sns.heatmap(medication_occ_corr, cmap='viridis', annot=True, fmt='d', ax=ax3)
        ax3.set_xlabel('Occupation')
        ax3.set_ylabel('Medications')
        ax3.set_title('Heatmap: Medications vs. Occupation')
        st.pyplot(fig3)
        

if __name__ == '__main__':
    main()
