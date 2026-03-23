"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-02-24
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0001_initial_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=100), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.Enum("admin", "viewer", name="userrole"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)

    op.create_table(
        "kri_definitions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("category", sa.String(length=255), nullable=False),
        sa.Column("sub_category", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("category", "sub_category", name="uq_kri_category_subcategory"),
    )
    op.create_index(op.f("ix_kri_definitions_category"), "kri_definitions", ["category"], unique=False)
    op.create_index(op.f("ix_kri_definitions_sub_category"), "kri_definitions", ["sub_category"], unique=False)

    op.create_table(
        "source_files",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("sha256", sa.String(length=64), nullable=False),
        sa.Column("row_count", sa.Integer(), nullable=False),
        sa.Column("uploaded_by_id", sa.Integer(), nullable=True),
        sa.Column("errors", sa.Text(), nullable=True),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["uploaded_by_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_source_files_sha256"), "source_files", ["sha256"], unique=True)
    op.create_index(op.f("ix_source_files_uploaded_at"), "source_files", ["uploaded_at"], unique=False)

    op.create_table(
        "kri_observations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("kri_definition_id", sa.Integer(), nullable=False),
        sa.Column("source_file_id", sa.Integer(), nullable=False),
        sa.Column("entry_date", sa.Date(), nullable=False),
        sa.Column("current_value", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["kri_definition_id"], ["kri_definitions.id"]),
        sa.ForeignKeyConstraint(["source_file_id"], ["source_files.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("kri_definition_id", "entry_date", "source_file_id", name="uq_kri_observation"),
    )
    op.create_index(op.f("ix_kri_observations_entry_date"), "kri_observations", ["entry_date"], unique=False)
    op.create_index(op.f("ix_kri_observations_kri_definition_id"), "kri_observations", ["kri_definition_id"], unique=False)
    op.create_index(op.f("ix_kri_observations_source_file_id"), "kri_observations", ["source_file_id"], unique=False)

    op.create_table(
        "kri_thresholds",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("kri_definition_id", sa.Integer(), nullable=False),
        sa.Column("method", sa.String(length=40), nullable=False),
        sa.Column("amber_percentile", sa.Float(), nullable=False),
        sa.Column("red_percentile", sa.Float(), nullable=False),
        sa.Column("amber_value", sa.Float(), nullable=True),
        sa.Column("red_value", sa.Float(), nullable=True),
        sa.Column("baseline_start", sa.Date(), nullable=False),
        sa.Column("baseline_end", sa.Date(), nullable=False),
        sa.Column("computed_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["kri_definition_id"], ["kri_definitions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_kri_thresholds_kri_definition_id"), "kri_thresholds", ["kri_definition_id"], unique=False)

    op.create_table(
        "kri_breaches",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("observation_id", sa.Integer(), nullable=False),
        sa.Column("threshold_id", sa.Integer(), nullable=False),
        sa.Column("threshold_version", sa.Integer(), nullable=False),
        sa.Column("severity", sa.String(length=16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["observation_id"], ["kri_observations.id"]),
        sa.ForeignKeyConstraint(["threshold_id"], ["kri_thresholds.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_kri_breaches_observation_id"), "kri_breaches", ["observation_id"], unique=False)
    op.create_index(op.f("ix_kri_breaches_severity"), "kri_breaches", ["severity"], unique=False)
    op.create_index(op.f("ix_kri_breaches_threshold_id"), "kri_breaches", ["threshold_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_kri_breaches_threshold_id"), table_name="kri_breaches")
    op.drop_index(op.f("ix_kri_breaches_severity"), table_name="kri_breaches")
    op.drop_index(op.f("ix_kri_breaches_observation_id"), table_name="kri_breaches")
    op.drop_table("kri_breaches")
    op.drop_index(op.f("ix_kri_thresholds_kri_definition_id"), table_name="kri_thresholds")
    op.drop_table("kri_thresholds")
    op.drop_index(op.f("ix_kri_observations_source_file_id"), table_name="kri_observations")
    op.drop_index(op.f("ix_kri_observations_kri_definition_id"), table_name="kri_observations")
    op.drop_index(op.f("ix_kri_observations_entry_date"), table_name="kri_observations")
    op.drop_table("kri_observations")
    op.drop_index(op.f("ix_source_files_uploaded_at"), table_name="source_files")
    op.drop_index(op.f("ix_source_files_sha256"), table_name="source_files")
    op.drop_table("source_files")
    op.drop_index(op.f("ix_kri_definitions_sub_category"), table_name="kri_definitions")
    op.drop_index(op.f("ix_kri_definitions_category"), table_name="kri_definitions")
    op.drop_table("kri_definitions")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    sa.Enum(name="userrole").drop(op.get_bind(), checkfirst=False)
