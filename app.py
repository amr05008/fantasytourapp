import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import API client for procyclingstats data
from api_client import (
    fetch_fantasy_standings,
    fetch_stage_by_stage_data,
    seconds_to_time_str,
    time_str_to_seconds
)
from team_config import TEAM_ROSTERS, RACE_CONFIG

# Page configuration
st.set_page_config(
    page_title="Sunshine Fantasy Tour de France 2025",
    page_icon="🚴",
    layout="wide"
)

# Enhanced Meta Tags for URL Sharing (Open Graph, Twitter Cards, Schema.org)
st.markdown("""
    <meta property="og:title" content="Sunshine Fantasy Tour de France 2025 - Live Results" />
    <meta property="og:description" content="Sunshine Fantasy Tour de France 2025" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://tdf2025.replit.app/" />
    <meta property="og:image" content="attached_assets/ChatGPT Image Jul 22, 2025, 02_24_08 PM_1753208677017.png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:locale" content="en_US" />
    <meta property="og:site_name" content="Fantasy Tour de France 2025" />
    
    <!-- Twitter Cards -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="Sunshine Fantasy Tour de France 2025" />
    <meta name="twitter:description" content="Sunshine Fantasy Tour de France 2025" />
    <meta name="twitter:image" content="attached_assets/ChatGPT Image Jul 22, 2025, 02_24_08 PM_1753208677017.png" />
    
    <!-- Schema.org Structured Data -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Sunshine Fantasy Tour de France 2025",
        "description": "Sunshine Fantasy Tour de France 2025",
        "url": "https://tdf2025.replit.app/",
        "applicationCategory": "SportsApplication",
        "operatingSystem": "Web Browser",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        },
        "author": {
            "@type": "Person",
            "name": "Aaron Roy"
        },
        "datePublished": "2025-07-22",
        "keywords": "Tour de France, Fantasy Sports, Cycling, Real-time Results, Sports Analytics"
    }
    </script>
    
    <!-- Additional meta tags for better indexing -->
    <meta name="description" content="Track real-time Fantasy Tour de France results with interactive standings, stage analysis, and team rosters. See who's wearing the yellow jersey!" />
    <meta name="keywords" content="Tour de France, Fantasy Sports, Cycling, Real-time Results, Sports Analytics, Yellow Jersey" />
    <meta name="author" content="Aaron Roy" />
    <meta name="robots" content="index, follow" />
    <meta name="theme-color" content="#1e1e1e" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    
    <!-- Favicon and Apple Touch Icons -->
    <link rel="icon" type="image/png" sizes="32x32" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚴</text></svg>" />
    <link rel="apple-touch-icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚴</text></svg>" />
""", unsafe_allow_html=True)

# Inject CSS with a custom background color
st.markdown(
    """
    <style>
    body {
            background-color: #1e1e1e;
            color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ====================
# COMPETITION CONFIGURATION
# ====================
# Toggle these settings to control winner display and completion status
COMPETITION_CONFIG = {
    "is_complete": True,  # Set to True when competition is finished
    "winner_name": "Aaron",  # Name of the competition winner
    "competition_name": "Tour de France 2025",
    "total_stages": 21,
    "completion_date": "July 27, 2025",
    "show_celebration": True  # Show celebration banner and styling
}

# Time conversion functions are now imported from api_client
# (time_str_to_seconds and seconds_to_time_str)

def calculate_time_gap(leader_time, participant_time):
    """Calculate time gap between leader and participant"""
    gap_seconds = participant_time - leader_time
    if gap_seconds == 0:
        return "Leader"
    return f"+{seconds_to_time_str(gap_seconds)}"

def create_winner_banner():
    """Create a celebration banner for the competition winner"""
    if not COMPETITION_CONFIG["is_complete"] or not COMPETITION_CONFIG["show_celebration"]:
        return
    
    winner = COMPETITION_CONFIG["winner_name"]
    competition = COMPETITION_CONFIG["competition_name"]
    completion_date = COMPETITION_CONFIG["completion_date"]
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 8px 32px rgba(255, 215, 0, 0.3);
        animation: celebrationPulse 2s ease-in-out infinite alternate;
        border: 3px solid #FF8C00;
    ">
        <h1 style="
            color: #000000;
            font-size: 2.5em;
            margin: 10px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            animation: bounce 1s ease-in-out infinite;
        ">
            🏆 {winner} WINS! 🏆
        </h1>
        <h3 style="
            color: #8B4513;
            margin: 10px 0;
            font-weight: bold;
        ">
            🚴 {competition} Champion! 🚴
        </h3>
        <p style="
            color: #000000;
            font-size: 1.2em;
            margin: 5px 0;
            font-weight: 600;
        ">
            Competition completed on {completion_date}
        </p>
        <div style="
            font-size: 2em;
            margin: 10px 0;
            animation: confetti 3s ease-in-out infinite;
        ">
            🎉 🎊 🥳 🎈 🎉
        </div>
    </div>
    
    <style>
    @keyframes celebrationPulse {{
        from {{
            transform: scale(1);
            box-shadow: 0 8px 32px rgba(255, 215, 0, 0.3);
        }}
        to {{
            transform: scale(1.02);
            box-shadow: 0 12px 40px rgba(255, 215, 0, 0.5);
        }}
    }}
    
    @keyframes bounce {{
        0%, 20%, 50%, 80%, 100% {{
            transform: translateY(0);
        }}
        40% {{
            transform: translateY(-10px);
        }}
        60% {{
            transform: translateY(-5px);
        }}
    }}
    
    @keyframes confetti {{
        0%, 100% {{
            transform: rotate(0deg);
        }}
        25% {{
            transform: rotate(5deg);
        }}
        75% {{
            transform: rotate(-5deg);
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

def get_competition_title():
    """Get the appropriate title based on competition status"""
    base_title = "🚴 Sunshine's Fantasy TDF 2025"
    
    if COMPETITION_CONFIG["is_complete"]:
        return f"{base_title} - COMPLETE ✅"
    else:
        return base_title

def create_completion_status_card():
    """Create a status card showing competition completion"""
    if not COMPETITION_CONFIG["is_complete"]:
        return
    
    winner = COMPETITION_CONFIG["winner_name"]
    total_stages = COMPETITION_CONFIG["total_stages"]
    completion_date = COMPETITION_CONFIG["completion_date"]
    
    st.markdown(f"""
    <div style="
        background-color: #2d2d2d;
        border: 2px solid #FFD700;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
        text-align: center;
    ">
        <h4 style="color: #FFD700; margin: 5px 0;">📊 Final Results</h4>
        <p style="color: #ffffff; margin: 5px 0;">
            All {total_stages} stages completed on {completion_date}
        </p>
        <p style="color: #FFD700; font-weight: bold; font-size: 1.1em; margin: 5px 0;">
            🏆 Champion: {winner}
        </p>
        <small style="color: #cccccc;">These are the final standings</small>
    </div>
    """, unsafe_allow_html=True)

def generate_share_content(data):
    """Generate dynamic content for social sharing based on current standings"""
    if data is None or len(data) == 0:
        return {
            'title': "Fantasy Tour de France 2025",
            'description': "Track real-time Fantasy Tour de France results with interactive standings and stage analysis!"
        }
    
    # Get current leader
    leader = data.iloc[0] if not data.empty else None
    total_stages = 21  # Tour de France standard
    
    if leader is not None:
        leader_name = leader.get('Name', 'Unknown')
        current_stage = 1  # You might want to calculate this from your data
        
        title = f"🚴 {leader_name} leads Fantasy Tour de France!"
        description = f"Stage {current_stage}/{total_stages} complete. Follow live standings, stage analysis, and team rosters in Sunshine's Fantasy Tour!"
    else:
        title = "Sunshine Fantasy Tour de France 2025"
        description = "Track real-time Fantasy Tour de France results with interactive standings, stage analysis, and team rosters!"
    
    return {
        'title': title,
        'description': description
    }

def create_sharing_buttons():
    """Create social media sharing buttons"""
    current_url = "https://your-app-url.replit.app"  # Replace with actual URL
    
    st.markdown("### 📱 Share This App")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        twitter_url = f"https://twitter.com/intent/tweet?url={current_url}&text=Check out Fantasy Tour de France 2025 results! 🚴⚡"
        st.markdown(f"[🐦 Tweet]({twitter_url})", unsafe_allow_html=True)
    
    with col2:
        facebook_url = f"https://www.facebook.com/sharer/sharer.php?u={current_url}"
        st.markdown(f"[👥 Facebook]({facebook_url})", unsafe_allow_html=True)
    
    with col3:
        linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url={current_url}"
        st.markdown(f"[💼 LinkedIn]({linkedin_url})", unsafe_allow_html=True)
    
    with col4:
        # Copy to clipboard button (using JavaScript)
        st.markdown(f"""
        <button onclick="navigator.clipboard.writeText('{current_url}'); alert('Link copied to clipboard!');" 
                style="background-color: #2d2d2d; color: white; border: 1px solid #555; padding: 5px 10px; border-radius: 4px; cursor: pointer;">
            📋 Copy Link
        </button>
        """, unsafe_allow_html=True)

# Data fetching functions replaced by API client
# (fetch_fantasy_standings and fetch_stage_by_stage_data from api_client)

def create_cumulative_time_chart(stage_data, latest_stage):
    """Create cumulative time progression chart"""
    fig = go.Figure()
    
    # Color scheme for participants
    colors = {
        'Jeremy': '#FFD700',  # Gold for leader styling
        'Leo': '#FF6B6B',
        'Charles': '#4ECDC4', 
        'Aaron': '#45B7D1',
        'Nate': '#96CEB4'
    }
    
    for participant, stages in stage_data.items():
        if stages:  # Only show participants with data
            stages_list = []
            times_list = []
            
            for stage in range(1, latest_stage + 1):
                if stage in stages:
                    stages_list.append(stage)
                    times_list.append(stages[stage]['time_seconds'] / 3600)  # Convert to hours
            
            if stages_list:
                # Create custom hover text with exact times
                hover_text = []
                for stage in stages_list:
                    time_str = stages[stage]['time']
                    hover_text.append(f'<b>{participant}</b><br>Stage: {stage}<br>Cumulative Time: {time_str}')
                
                fig.add_trace(go.Scatter(
                    x=stages_list,
                    y=times_list,
                    mode='lines+markers',
                    name=participant,
                    line=dict(color=colors.get(participant, '#FFFFFF'), width=3),
                    marker=dict(size=8, color=colors.get(participant, '#FFFFFF')),
                    hovertemplate='%{text}<extra></extra>',
                    text=hover_text
                ))
    
    # Dark theme styling with mobile responsiveness
    fig.update_layout(
        title={
            'text': 'Cumulative Time Progression by Stage',
            'x': 0.5,
            'font': {'size': 18, 'color': '#FFFFFF'}
        },
        xaxis_title='Stage',
        yaxis_title='Cumulative Time (Hours)',
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font=dict(color='#FFFFFF', size=12),
        xaxis=dict(
            gridcolor='#404040',
            tickmode='linear',
            dtick=1,
            range=[0.5, latest_stage + 0.5],
            tickfont=dict(color='#FFFFFF', size=10),
            title=dict(font=dict(color='#FFFFFF', size=12))
        ),
        yaxis=dict(
            gridcolor='#404040',
            tickfont=dict(color='#FFFFFF', size=10),
            title=dict(font=dict(color='#FFFFFF', size=12))
        ),
        legend=dict(
            font=dict(color='#FFFFFF', size=12),
            bgcolor='rgba(45, 45, 45, 0.9)',
            bordercolor='#404040',
            borderwidth=1,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=40, r=40, t=80, b=40),
        height=350
    )
    
    return fig

def create_stage_performance_chart(stage_data, latest_stage):
    """Create individual stage performance chart"""
    # Calculate stage-specific times (time between stages)
    stage_performance = {}
    stage_performance_seconds = {}
    
    for participant, stages in stage_data.items():
        stage_performance[participant] = {}
        stage_performance_seconds[participant] = {}
        prev_time = 0
        
        for stage in range(1, latest_stage + 1):
            if stage in stages:
                current_time = stages[stage]['time_seconds']
                if stage == 1:
                    stage_time = current_time
                else:
                    stage_time = current_time - prev_time
                stage_performance[participant][stage] = stage_time / 60  # Convert to minutes for y-axis
                stage_performance_seconds[participant][stage] = stage_time  # Keep seconds for hover text
                prev_time = current_time
    
    # Create subplot for each stage
    fig = make_subplots(
        rows=1, cols=min(latest_stage, 5),  # Show max 5 stages at once
        subplot_titles=[f'Stage {i}' for i in range(max(1, latest_stage-4), latest_stage + 1)]
    )
    
    colors = {
        'Jeremy': '#FFD700',
        'Leo': '#FF6B6B', 
        'Charles': '#4ECDC4',
        'Aaron': '#45B7D1',
        'Nate': '#96CEB4'
    }
    
    stages_to_show = list(range(max(1, latest_stage-4), latest_stage + 1))
    
    for col, stage in enumerate(stages_to_show, 1):
        participants = []
        times = []
        bar_colors = []
        hover_texts = []
        
        for participant in stage_performance:
            if stage in stage_performance[participant]:
                participants.append(participant)
                times.append(stage_performance[participant][stage])
                bar_colors.append(colors.get(participant, '#FFFFFF'))
                
                # Convert seconds to H:MM:SS format for hover
                stage_seconds = stage_performance_seconds[participant][stage]
                stage_time_str = seconds_to_time_str(int(stage_seconds))
                hover_texts.append(f'<b>{participant}</b><br>Stage {stage} Time: {stage_time_str}')
        
        if participants:
            fig.add_trace(
                go.Bar(
                    x=participants,
                    y=times,
                    name=f'Stage {stage}',
                    marker_color=bar_colors,
                    showlegend=False,
                    hovertemplate='%{text}<extra></extra>',
                    text=hover_texts
                ),
                row=1, col=col
            )
    
    # Dark theme styling
    fig.update_layout(
        title={
            'text': 'Individual Stage Performance (Minutes)',
            'x': 0.5,
            'font': {'size': 16, 'color': '#FFFFFF'}
        },
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font=dict(color='#FFFFFF', size=11),
        margin=dict(l=30, r=30, t=70, b=30),
        height=350
    )
    
    # Update all subplot axes and annotations
    for i in range(1, min(latest_stage, 5) + 1):
        fig.update_xaxes(
            tickangle=45,
            gridcolor='#404040',
            tickfont=dict(color='#FFFFFF'),
            row=1, col=i
        )
        fig.update_yaxes(
            gridcolor='#404040',
            tickfont=dict(color='#FFFFFF'),
            row=1, col=i
        )
    
    # Update subplot titles color - use layout update method
    try:
        # Update annotations via layout update to avoid direct access issues
        current_annotations = getattr(fig.layout, 'annotations', None)
        if current_annotations:
            fig.update_layout(
                annotations=[
                    dict(
                        text=getattr(annotation, 'text', ''),
                        x=getattr(annotation, 'x', 0.5),
                        y=getattr(annotation, 'y', 1),
                        xref=getattr(annotation, 'xref', 'paper'),
                        yref=getattr(annotation, 'yref', 'paper'),
                        font=dict(color='#FFFFFF', size=14)
                    ) for annotation in current_annotations
                ]
            )
    except Exception:
        pass  # Skip if annotations not available
    
    return fig

def create_gap_evolution_chart(stage_data, latest_stage):
    """Create chart showing gap evolution relative to leader"""
    fig = go.Figure()
    
    colors = {
        'Jeremy': '#FFD700',
        'Leo': '#FF6B6B',
        'Charles': '#4ECDC4',
        'Aaron': '#45B7D1', 
        'Nate': '#96CEB4'
    }
    
    # Find leader at each stage and calculate gaps
    for participant, stages in stage_data.items():
        if stages:
            stages_list = []
            gaps_list = []
            
            for stage in range(1, latest_stage + 1):
                if stage in stages:
                    # Find leader time for this stage
                    leader_time = min([
                        stage_data[p][stage]['time_seconds'] 
                        for p in stage_data 
                        if stage in stage_data[p]
                    ])
                    
                    gap_seconds = stages[stage]['time_seconds'] - leader_time
                    stages_list.append(stage)
                    gaps_list.append(gap_seconds / 60)  # Convert to minutes
            
            if stages_list and any(gap > 0 for gap in gaps_list):  # Don't show leader line
                # Create custom hover text with exact gap times
                hover_text = []
                for i, stage in enumerate(stages_list):
                    gap_seconds = gaps_list[i] * 60  # Convert back to seconds
                    gap_time_str = calculate_time_gap(0, int(gap_seconds))  # Format as "+H:MM:SS"
                    hover_text.append(f'<b>{participant}</b><br>Stage: {stage}<br>Gap to Leader: {gap_time_str}')
                
                fig.add_trace(go.Scatter(
                    x=stages_list,
                    y=gaps_list,
                    mode='lines+markers',
                    name=participant,
                    line=dict(color=colors.get(participant, '#FFFFFF'), width=3),
                    marker=dict(size=8, color=colors.get(participant, '#FFFFFF')),
                    hovertemplate='%{text}<extra></extra>',
                    text=hover_text
                ))
    
    # Dark theme styling with mobile responsiveness
    fig.update_layout(
        title={
            'text': 'Time Gap Evolution (Minutes Behind Leader)',
            'x': 0.5,
            'font': {'size': 16, 'color': '#FFFFFF'}
        },
        xaxis_title='Stage',
        yaxis_title='Gap to Leader (Minutes)',
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font=dict(color='#FFFFFF', size=11),
        xaxis=dict(
            gridcolor='#404040',
            tickmode='linear',
            dtick=1,
            range=[0.5, latest_stage + 0.5],
            tickfont=dict(color='#FFFFFF', size=10),
            title=dict(font=dict(color='#FFFFFF', size=12))
        ),
        yaxis=dict(
            gridcolor='#404040',
            tickfont=dict(color='#FFFFFF', size=10),
            title=dict(font=dict(color='#FFFFFF', size=12))
        ),
        legend=dict(
            font=dict(color='#FFFFFF', size=12),
            bgcolor='rgba(45, 45, 45, 0.9)',
            bordercolor='#404040',
            borderwidth=1,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=40, r=40, t=70, b=40),
        height=350
    )
    
    return fig

def create_riders_display(rider_details):
    """Create the team riders display with cards for each team

    Args:
        rider_details: Dictionary mapping participants to their rider details
    """
    if not rider_details:
        st.error("No rider data available")
        return

    # Color scheme for team cards (matching the existing chart colors)
    team_colors = {
        'Jeremy': '#FFD700',  # Gold
        'Leo': '#FF6B6B',     # Red
        'Charles': '#4ECDC4',  # Teal
        'Aaron': '#45B7D1',   # Blue
        'Nate': '#96CEB4'     # Green
    }

    st.markdown("### 👥 Team Rosters")
    st.markdown("Current riders for each fantasy team with real-time GC standings")

    # Create responsive team display
    teams_list = list(rider_details.items())

    # Use responsive columns that work better on mobile
    if len(teams_list) <= 2:
        cols = st.columns(len(teams_list))
        display_teams = [teams_list]
    else:
        # Split teams into rows of 2-3 for mobile compatibility
        display_teams = [teams_list[:2]]
        if len(teams_list) > 2:
            display_teams.append(teams_list[2:4])
        if len(teams_list) == 5:
            display_teams.append([teams_list[4]])

    for row_teams in display_teams:
        if len(row_teams) == 1:
            cols = st.columns(1)
        else:
            cols = st.columns(len(row_teams))

        for col_idx, (team_owner, riders) in enumerate(row_teams):
            with cols[col_idx]:
                # Get team color
                color = team_colors.get(team_owner, '#333333')

                # Display team header
                st.markdown(f"### 🚴 {team_owner}")
                st.markdown(f"<div style='color: {color}; font-weight: bold; margin-bottom: 10px;'>{len(riders)} Riders</div>", unsafe_allow_html=True)

                # Display riders with GC info
                if riders:
                    for i, rider_info in enumerate(riders, 1):
                        rider_name = rider_info.get('name', 'Unknown')
                        rider_time = rider_info.get('time', 'N/A')
                        rider_rank = rider_info.get('rank', '-')

                        if rider_time == 'DNF':
                            st.write(f"{i}. {rider_name} - ❌ DNF/DNS")
                        else:
                            st.write(f"{i}. {rider_name}")
                            st.write(f"   GC: #{rider_rank} - {rider_time}")
                else:
                    st.write("No riders assigned")

                st.markdown("---")

    # Add summary statistics
    st.markdown("---")

    # Create responsive summary row
    total_riders = sum(len(riders) for riders in rider_details.values())
    avg_riders = total_riders / len(rider_details) if rider_details else 0

    # Count active riders (not DNF)
    active_riders = sum(
        1 for riders in rider_details.values()
        for rider in riders
        if rider.get('time', 'DNF') != 'DNF'
    )

    # Use 2 columns for mobile, 3 for desktop
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Riders", total_riders)
    with col2:
        st.metric("Active in Race", active_riders)
    with col3:
        st.metric("Teams", len(rider_details))

def get_dark_theme_css():
    """Return dark theme CSS with animated transitions"""
    return """
    <style>
    /* Global animations and transitions */
    * {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
        transition: background-color 0.3s ease;
    }
    .stMarkdown {
        background-color: #1e1e1e;
        color: #ffffff;
        transition: opacity 0.3s ease, transform 0.3s ease;
    }
    .element-container {
        background-color: #1e1e1e;
        transition: all 0.3s ease;
    }
    
    /* Animated cards with hover effects */
    .dark-card {
        background-color: #2d2d2d !important;
        border: 2px solid #404040 !important;
        color: #ffffff !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        transform: translateY(0);
    }
    .dark-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.3) !important;
        border-color: #606060 !important;
    }
    
    .dark-leader-card {
        background-color: #FFD700 !important;
        color: #000000 !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        transform: translateY(0);
        animation: leaderGlow 2s ease-in-out infinite alternate;
    }
    .dark-leader-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(255, 215, 0, 0.4) !important;
    }
    
    /* Leader glow animation */
    @keyframes leaderGlow {
        from {
            box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 0 20px rgba(255, 215, 0, 0.3);
        }
        to {
            box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 0 30px rgba(255, 215, 0, 0.5);
        }
    }
    .stMetric {
        background-color: #2d2d2d;
        border-radius: 8px;
        padding: 15px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        transform: translateY(0);
    }
    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
        background-color: #353535;
    }
    .stMetric > div {
        color: #ffffff;
        transition: color 0.3s ease;
    }
    .stProgress > div > div > div > div {
        background-color: #404040;
        transition: all 0.3s ease;
    }
    .stProgress > div > div > div > div > div {
        background-color: #FFD700 !important;
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        animation: progressPulse 1.5s ease-in-out infinite alternate;
    }
    
    /* Progress bar animation */
    @keyframes progressPulse {
        from {
            box-shadow: 0 0 5px rgba(255, 215, 0, 0.3);
        }
        to {
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
        }
    }
    .stInfo {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    .stInfo > div {
        color: #ffffff !important;
    }
    .stButton > button {
        background-color: #404040 !important;
        color: #ffffff !important;
        border: 1px solid #606060 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        transform: translateY(0);
    }
    .stButton > button:hover {
        background-color: #505050 !important;
        border: 1px solid #707070 !important;
        color: #ffffff !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .stButton > button:active {
        background-color: #606060 !important;
        color: #ffffff !important;
        transform: translateY(0);
        transition: all 0.1s ease;
    }
    /* Force button styling with higher specificity */
    div[data-testid="stButton"] > button {
        background-color: #404040 !important;
        color: #ffffff !important;
        border: 1px solid #606060 !important;
    }
    div[data-testid="stButton"] > button:hover {
        background-color: #505050 !important;
        color: #0000FF!important;
    }
    div[data-testid="stButton"] > button:focus {
        background-color: #404040 !important;
        color: #ffffff !important;
        box-shadow: 0 0 0 2px #FFD700 !important;
    }
    .stSpinner {
        color: #ffffff !important;
    }
    div[data-testid="stMarkdownContainer"] {
        color: #ffffff;
    }
    /* Animated Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #2d2d2d !important;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #404040 !important;
        color: #ffffff !important;
        border: 1px solid #606060 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        transform: translateY(0);
        position: relative;
        overflow: hidden;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #505050 !important;
        color: #ffffff !important;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFD700 !important;
        color: #000000 !important;
        border: 1px solid #FFD700 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
        animation: activeTabGlow 1s ease-in-out infinite alternate;
    }
    
    /* Active tab glow animation */
    @keyframes activeTabGlow {
        from {
            box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
        }
        to {
            box-shadow: 0 4px 20px rgba(255, 215, 0, 0.5);
        }
    }
    /* Animated Selectbox styling */
    .stSelectbox > div > div {
        background-color: #404040 !important;
        color: #ffffff !important;
        border: 1px solid #606060 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        transform: translateY(0);
    }
    .stSelectbox > div > div:hover {
        border-color: #707070 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        transform: translateY(-1px);
    }
    .stSelectbox > div > div > div {
        color: #ffffff !important;
        transition: color 0.3s ease;
    }
    .stSelectbox [data-baseweb="select"] {
        background-color: #404040 !important;
        transition: all 0.3s ease;
    }
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #404040 !important;
        color: #ffffff !important;
        transition: all 0.3s ease;
    }
    /* Animated Dropdown menu styling */
    .stSelectbox ul {
        background-color: #2d2d2d !important;
        border: 1px solid #606060 !important;
        animation: dropdownSlide 0.2s ease-out;
        transform-origin: top;
    }
    .stSelectbox li {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        transition: all 0.2s ease;
    }
    .stSelectbox li:hover {
        background-color: #404040 !important;
        color: #ffffff !important;
        transform: translateX(4px);
    }
    
    /* Dropdown slide animation */
    @keyframes dropdownSlide {
        from {
            opacity: 0;
            transform: scaleY(0.8);
        }
        to {
            opacity: 1;
            transform: scaleY(1);
        }
    }
    /* Info box styling improvements */
    .stAlert {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border: 1px solid #404040 !important;
    }
    .stAlert > div {
        color: #ffffff !important;
    }
    /* Text elements */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #ffffff !important;
    }
    .stMarkdown p {
        color: #ffffff !important;
    }
    .stMarkdown strong {
        color: #ffffff !important;
    }
    .stMarkdown em {
        color: #e0e0e0 !important;
    }
    /* Additional button overrides to prevent white background inheritance */
    button[kind="secondary"] {
        background-color: #404040 !important;
        color: #ffffff !important;
        border: 1px solid #606060 !important;
    }
    button[kind="secondary"]:hover {
        background-color: #505050 !important;
        color: #ffffff !important;
    }
    button[data-testid*="button"] {
        background-color: #404040 !important;
        color: #ffffff !important;
        border: 1px solid #606060 !important;
    }
    button[data-testid*="button"]:hover {
        background-color: #505050 !important;
        color: #ffffff !important;
    }
    /* Override any inherited white backgrounds */
    .stButton button[style*="background"] {
        background-color: #404040 !important;
        color: #ffffff !important;
    }
    /* Universal button override for all states */
    button {
        background-color: #404040 !important;
        color: #ffffff !important;
        border: 1px solid #606060 !important;
    }
    button:hover {
        background-color: #505050 !important;
        color: #ffffff !important;
    }
    button:focus {
        background-color: #404040 !important;
        color: #ffffff !important;
        outline: 2px solid #FFD700 !important;
    }
    button:active {
        background-color: #606060 !important;
        color: #ffffff !important;
    }
    /* Specific targeting for refresh button and all Streamlit buttons */
    .stButton > button,
    button[data-testid="baseButton-secondary"],
    button[kind="secondary"],
    [data-testid="stButton"] button {
        background-color: #404040 !important;
        color: #ffffff !important;
        border: 1px solid #606060 !important;
    }
    .stButton > button:hover,
    button[data-testid="baseButton-secondary"]:hover,
    button[kind="secondary"]:hover,
    [data-testid="stButton"] button:hover {
        background-color: #505050 !important;
        color: #ffffff !important;
        border: 1px solid #707070 !important;
    }
    /* Additional hover state overrides with maximum specificity */
    div[data-testid="stButton"] > button:hover,
    div[data-testid="column"] div[data-testid="stButton"] > button:hover,
    .stButton button:hover,
    button[title*="Refresh"]:hover,
    button[aria-label*="Refresh"]:hover {
        background-color: #505050 !important;
        color: #ffffff !important;
        border: 1px solid #707070 !important;
        box-shadow: none !important;
    }
    /* Force override any inline styles or computed styles */
    button:hover[style] {
        background-color: #505050 !important;
        color: #ffffff !important;
    }
    /* Legend and analysis text styling */
    .legend-text, .analysis-text {
        color: #ffffff !important;
        font-weight: bold !important;
    }
    .legend-description, .analysis-description {
        color: #e0e0e0 !important;
    }
    /* Universal text color overrides */
    p, span, div {
        color: #ffffff !important;
    }
    small, .small-text {
        color: #e0e0e0 !important;
    }
    /* Footer text styling */
    .stMarkdown em, .stMarkdown i, em, i {
        color: #b0b0b0 !important;
    }
    
    /* Content fade-in animations */
    .stContainer {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Spinner animation improvements */
    .stSpinner > div {
        animation: spinnerBounce 1.2s ease-in-out infinite;
    }
    
    /* Chart container animations */
    .stPlotlyChart {
        animation: chartFadeIn 0.8s ease-out;
    }
    
    /* Content animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes chartFadeIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes spinnerBounce {
        0%, 20%, 53%, 80%, 100% {
            transform: translateY(0);
        }
        40%, 43% {
            transform: translateY(-8px);
        }
        70% {
            transform: translateY(-4px);
        }
        90% {
            transform: translateY(-2px);
        }
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Hover zoom effect for stage indicators */
    .stage-indicator {
        display: inline-block;
        transition: transform 0.2s ease;
    }
    .stage-indicator:hover {
        transform: scale(1.2);
    }
    
    /* Mobile Responsive Design */
    @media (max-width: 768px) {
        /* Mobile layout adjustments */
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 100% !important;
        }
        
        /* Mobile typography */
        h1 {
            font-size: 1.8rem !important;
            text-align: center !important;
        }
        
        h2, h3 {
            font-size: 1.3rem !important;
        }
        
        /* Mobile cards */
        .dark-card, .dark-leader-card {
            margin: 4px 0 !important;
            padding: 12px !important;
            font-size: 14px !important;
        }
        
        .dark-leader-card span {
            font-size: 18px !important;
        }
        
        .dark-card span {
            font-size: 16px !important;
        }
        
        /* Mobile metrics - stack vertically */
        .stMetric {
            margin-bottom: 1rem !important;
            text-align: center !important;
        }
        
        /* Mobile tabs */
        .stTabs [data-baseweb="tab"] {
            font-size: 12px !important;
            padding: 8px 12px !important;
            min-height: 44px !important;
        }
        
        /* Mobile buttons - larger touch targets */
        .stButton > button {
            min-height: 44px !important;
            font-size: 14px !important;
            padding: 12px 16px !important;
        }
        
        /* Mobile selectbox */
        .stSelectbox > div > div {
            min-height: 44px !important;
            font-size: 14px !important;
        }
        
        /* Mobile stage indicators - wrap and space better */
        .stage-indicator {
            font-size: 20px !important;
            margin: 2px !important;
        }
        
        /* Mobile progress bar */
        .stProgress {
            height: 12px !important;
        }
        
        /* Mobile charts */
        .stPlotlyChart {
            height: 300px !important;
        }
        
        /* Hide hover effects on mobile */
        .dark-card:hover,
        .dark-leader-card:hover,
        .stMetric:hover,
        .stage-indicator:hover {
            transform: none !important;
            box-shadow: none !important;
        }
        
        /* Mobile column adjustments */
        .row-widget.stHorizontal > div {
            flex: 1 1 100% !important;
            margin-bottom: 0.5rem !important;
        }
    }
    
    @media (max-width: 480px) {
        /* Extra small mobile devices */
        h1 {
            font-size: 1.5rem !important;
        }
        
        .dark-card, .dark-leader-card {
            padding: 10px !important;
            font-size: 12px !important;
        }
        
        .dark-leader-card span {
            font-size: 16px !important;
        }
        
        .dark-card span {
            font-size: 14px !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-size: 10px !important;
            padding: 6px 8px !important;
        }
        
        .stage-indicator {
            font-size: 16px !important;
        }
        
        .stPlotlyChart {
            height: 250px !important;
        }
    }
    
    /* Touch-friendly interactions */
    @media (pointer: coarse) {
        .stButton > button,
        .stSelectbox > div > div,
        .stTabs [data-baseweb="tab"] {
            min-height: 44px !important;
        }
        
        /* Disable hover animations on touch devices */
        .dark-card:hover,
        .dark-leader-card:hover,
        .stMetric:hover,
        .stButton > button:hover,
        .stage-indicator:hover {
            transform: none !important;
        }
    }
    </style>
    """

def main():
    # Apply dark theme CSS
    st.markdown(get_dark_theme_css(), unsafe_allow_html=True)
    
    # Display winner banner if competition is complete
    create_winner_banner()
    
    # Title and header (dynamic based on completion status)
    st.title(get_competition_title())
    
    # Display completion status card if competition is complete
    create_completion_status_card()
    
    # Subtitle
    if COMPETITION_CONFIG["is_complete"]:
        st.markdown("### 🏁 Final Standings")
    else:
        st.markdown("### General Classification Standings")
    
    # Add refresh button with mobile-friendly layout
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🔄 Refresh", help="Refresh data from procyclingstats API", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    # Fetch and process data from procyclingstats API
    with st.spinner("Fetching latest standings from procyclingstats..."):
        fantasy_data = fetch_fantasy_standings()

    if fantasy_data is None:
        st.error("Unable to load standings data. Please check the API connection or ensure race data is available.")
        st.info("💡 Make sure team rosters are configured in team_config.py and the race has started.")
        return

    sorted_participants = fantasy_data['standings']
    latest_stage = fantasy_data['latest_stage']
    rider_details = fantasy_data['rider_details']

    # Fetch stage-by-stage data for charts
    stage_by_stage_data = fetch_stage_by_stage_data(latest_stage)
    
    # Create main navigation tabs
    tab1, tab2, tab3 = st.tabs(["🏆 Current Standings", "📊 Stage Analysis", "👥 Team Riders"])
    
    with tab1:
        # Create standings table - moved to top
        st.markdown("### 🏆 Current Standings")
        
        # Custom CSS for Tour de France styling
        st.markdown("""
        <style>
        .leader-row {
            background-color: #FFD700 !important;
            font-weight: bold;
        }
        .standings-table {
            font-size: 16px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display standings
        for i, (participant, data) in enumerate(sorted_participants):
            position = data['position']
            time_str = data['total_time']  # Changed from 'time' to 'total_time'
            gap = data['gap']
            
            # Create columns for the display
            pos_col, name_col, time_col, gap_col = st.columns([1, 3, 2, 2])
            
            # Apply yellow background for leader
            if position == 1:
                # Dynamic label based on competition status
                leader_label = "🏆 CHAMPION" if COMPETITION_CONFIG["is_complete"] else "👑 LEADER"
                container = st.container()
                with container:
                    st.markdown(f"""
                    <div class="dark-leader-card" style="background-color: #FFD700; padding: 15px; border-radius: 8px; margin: 8px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 24px; font-weight: bold; color: #000000;">🥇 {position}. {participant}</span>
                            <span style="font-size: 20px; font-weight: bold; color: #000000;">{time_str}</span>
                            <span style="font-size: 18px; color: #B8860B; font-weight: bold;">{leader_label}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # Regular participant display
                total_participants = len(sorted_participants)
                if position == total_participants:
                    # Last place gets sad panda
                    medal = f"{position}. 🐼"
                elif position == 2:
                    medal = "🥈"
                elif position == 3:
                    medal = "🥉"
                else:
                    medal = f"{position}."
                
                st.markdown(f"""
                <div class="dark-card" style="background-color: #2d2d2d; padding: 15px; border-radius: 8px; margin: 8px 0; border: 2px solid #404040; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 22px; font-weight: bold; color: #ffffff;">{medal} {participant}</span>
                        <span style="font-size: 18px; font-weight: 600; color: #e0e0e0;">{time_str}</span>
                        <span style="font-size: 16px; color: #ff6b6b; font-weight: 600;">{gap}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Additional information with mobile-responsive layout
        st.markdown("---")
        # Use different column layouts for mobile vs desktop
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            total_participants = len(sorted_participants)
            st.metric("Total Participants", total_participants)
        
        with col2:
            leader_name = sorted_participants[0][0]
            leader_title = "Champion" if COMPETITION_CONFIG["is_complete"] else "Current Leader"
            st.metric(leader_title, leader_name)
        
        with col3:
            if len(sorted_participants) > 1:
                gap_to_second = sorted_participants[1][1]['gap']
                st.metric("Gap to 2nd Place", gap_to_second)
            else:
                st.metric("Gap to 2nd Place", "N/A")
        
        # Stage Progress Visualization (moved below standings)
        st.markdown("---")
        st.info(f"📊 Current standings after Stage {latest_stage}")
        
        total_stages = 21
        progress_percentage = (latest_stage / total_stages) * 100
        remaining_stages = total_stages - latest_stage
        
        # Create progress bar section with mobile layout
        st.markdown("### 🏁 Tour Progress")
        
        # Progress bar takes full width on mobile
        st.progress(progress_percentage / 100)
        st.markdown(f"**Stage {latest_stage} of {total_stages}** ({progress_percentage:.1f}% complete)")
        
        # Metrics in responsive columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Stages Completed", latest_stage, delta=None)
        
        with col2:
            st.metric("Stages Remaining", remaining_stages, delta=None)
        
        # Visual stage indicator with mobile-friendly wrapping
        st.markdown("#### Stage Status")
        stage_indicators = ""
        for stage in range(1, total_stages + 1):
            if stage <= latest_stage:
                stage_indicators += '<span class="stage-indicator">🟢</span> '  # Completed stages
            elif stage == latest_stage + 1:
                stage_indicators += '<span class="stage-indicator">🔴</span> '  # Next stage
            else:
                stage_indicators += '<span class="stage-indicator">⚪</span> '  # Future stages
        
        st.markdown(f'<p class="legend-text" style="color: #ffffff !important; font-weight: bold;">Stages 1-21:</p><div style="color: #ffffff !important; font-size: 18px; line-height: 1.5; word-wrap: break-word;">{stage_indicators}</div>', unsafe_allow_html=True)
        st.markdown('<p class="legend-description" style="color: #e0e0e0 !important; font-size: 14px;">🟢 Completed | 🔴 Next | ⚪ Future</p>', unsafe_allow_html=True)
        
        # Footer
        st.markdown("---")
        st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Data refreshes every 5 minutes*")
        st.markdown("*🟡 Yellow highlight indicates the current General Classification leader*")
    
    with tab2:
        # Stage Analysis Charts
        st.markdown("### 📊 Stage-by-Stage Performance Analysis")
        
        if latest_stage > 1 and stage_by_stage_data:
            # Create chart selection
            chart_option = st.selectbox(
                "Select Analysis View:",
                [
                    "🏁 Cumulative Time Progression",
                    "⚡ Individual Stage Performance", 
                    "📈 Gap Evolution from Leader"
                ]
            )
            
            if chart_option == "🏁 Cumulative Time Progression":
                st.plotly_chart(
                    create_cumulative_time_chart(stage_by_stage_data, latest_stage),
                    use_container_width=True
                )
                st.markdown('<p class="analysis-text" style="color: #ffffff !important; font-weight: bold;">Analysis:</p><p class="analysis-description" style="color: #e0e0e0 !important;">Shows each participant\'s total cumulative time progression across all completed stages.</p>', unsafe_allow_html=True)
                
            elif chart_option == "⚡ Individual Stage Performance":
                st.plotly_chart(
                    create_stage_performance_chart(stage_by_stage_data, latest_stage),
                    use_container_width=True
                )
                st.markdown('<p class="analysis-text" style="color: #ffffff !important; font-weight: bold;">Analysis:</p><p class="analysis-description" style="color: #e0e0e0 !important;">Displays individual stage times to identify stage winners and performance patterns.</p>', unsafe_allow_html=True)
                
            elif chart_option == "📈 Gap Evolution from Leader":
                st.plotly_chart(
                    create_gap_evolution_chart(stage_by_stage_data, latest_stage),
                    use_container_width=True
                )
                st.markdown('<p class="analysis-text" style="color: #ffffff !important; font-weight: bold;">Analysis:</p><p class="analysis-description" style="color: #e0e0e0 !important;">Tracks how time gaps between participants and the leader evolve over stages.</p>', unsafe_allow_html=True)
        
        else:
            st.info("📊 Stage analysis will be available once multiple stages are completed.")
            st.markdown('<p style="color: #e0e0e0;">Current stage data is insufficient for detailed analysis. Charts will appear as more stage data becomes available.</p>', unsafe_allow_html=True)
    
    with tab3:
        # Team Riders Display
        if rider_details:
            create_riders_display(rider_details)
        else:
            st.error("Unable to load rider roster data. Please check the team configuration in team_config.py")
    
    # Add sharing section at the bottom of the application
    st.markdown("---")  # Add separator line
    with st.expander("📱 Share This App", expanded=False):
        create_sharing_buttons()

if __name__ == "__main__":
    main()
