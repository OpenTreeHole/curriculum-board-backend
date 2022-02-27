from base64 import b32encode
from hashlib import sha3_224
from typing import Type, Tuple, Optional

from tortoise import Model
from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel, PydanticListModel, \
    pydantic_queryset_creator


def pmc(
        cls: "Type[Model]",
        *,
        name: object = None,
        exclude: Tuple[str, ...] = (),
        include: Tuple[str, ...] = (),
        computed: Tuple[str, ...] = (),
        allow_cycles: Optional[bool] = None,
        sort_alphabetically: Optional[bool] = None,
        _stack: tuple = (),
        exclude_readonly: bool = False,
        meta_override: Optional[Type] = None,
) -> Type[PydanticModel]:
    """
    Function to build `Pydantic Model <https://pydantic-docs.helpmanual.io/usage/models/>`__ off Tortoise Model.

    :param cls: The Tortoise Model
    :param name: Specify a custom name explicitly, instead of a generated name.
    :param exclude: Extra fields to exclude from the provided model.
    :param include: Extra fields to include from the provided model.
    :param computed: Extra computed fields to include from the provided model.
    :param allow_cycles: Do we allow any cycles in the generated model?
        This is only useful for recursive/self-referential models.

        A value of ``False`` (the default) will prevent any and all backtracking.
    :param sort_alphabetically: Sort the parameters alphabetically instead of Field-definition order.

        The default order would be:

            * Field definition order +
            * order of reverse relations (as discovered) +
            * order of computed functions (as provided).
    :param exclude_readonly: Build a subset model that excludes any readonly fields
    :param meta_override: A PydanticMeta class to override model's values.
    """
    fqname = cls.__module__ + "." + cls.__qualname__
    postfix = ""

    def get_name() -> str:
        # If arguments are specified (different from the defaults), we append a hash to the
        # class name, to make it unique
        # We don't check by stack, as cycles get explicitly renamed.
        # When called later, include is explicitly set, so fence passes.
        nonlocal postfix
        is_default = (
                exclude == ()
                and include == ()
                and computed == ()
                and sort_alphabetically is None
                and allow_cycles is None
        )
        hashval = (
            f"{fqname};{exclude};{include};{computed};{_stack}:{sort_alphabetically}:{allow_cycles}"
        )
        postfix = (
            "." + b32encode(sha3_224(hashval.encode("utf-8")).digest()).decode("utf-8").lower()[:6]
            if not is_default
            else ""
        )
        return fqname + postfix

    return pydantic_model_creator(cls, name=name or get_name(), exclude=exclude, include=include, computed=computed,
                                  allow_cycles=allow_cycles, sort_alphabetically=sort_alphabetically,
                                  exclude_readonly=exclude_readonly, meta_override=meta_override)


def pqc(
        cls: "Type[Model]",
        *,
        name=None,
        exclude: Tuple[str, ...] = (),
        include: Tuple[str, ...] = (),
        computed: Tuple[str, ...] = (),
        allow_cycles: Optional[bool] = None,
        sort_alphabetically: Optional[bool] = None,
) -> Type[PydanticListModel]:
    """
    Function to build a `Pydantic Model <https://pydantic-docs.helpmanual.io/usage/models/>`__ list off Tortoise Model.

    :param cls: The Tortoise Model to put in a list.
    :param name: Specify a custom name explicitly, instead of a generated name.

        The list generated name is currently naive and merely adds a "s" to the end
        of the singular name.
    :param exclude: Extra fields to exclude from the provided model.
    :param include: Extra fields to include from the provided model.
    :param computed: Extra computed fields to include from the provided model.
    :param allow_cycles: Do we allow any cycles in the generated model?
        This is only useful for recursive/self-referential models.

        A value of ``False`` (the default) will prevent any and all backtracking.
    :param sort_alphabetically: Sort the parameters alphabetically instead of Field-definition order.

        The default order would be:

            * Field definition order +
            * order of reverse relations (as discovered) +
            * order of computed functions (as provided).
    """
    fqname = cls.__module__ + "." + cls.__qualname__
    postfix = ""

    def get_name() -> str:
        # If arguments are specified (different from the defaults), we append a hash to the
        # class name, to make it unique
        # We don't check by stack, as cycles get explicitly renamed.
        # When called later, include is explicitly set, so fence passes.
        nonlocal postfix
        is_default = (
                exclude == ()
                and include == ()
                and computed == ()
                and sort_alphabetically is None
                and allow_cycles is None
        )
        hashval = (
            f"{fqname};{exclude};{include};{computed};{sort_alphabetically}:{allow_cycles}"
        )
        postfix = (
            "." + b32encode(sha3_224(hashval.encode("utf-8")).digest()).decode("utf-8").lower()[:6]
            if not is_default
            else ""
        )
        return fqname + postfix

    return pydantic_queryset_creator(cls, name=name or get_name(), exclude=exclude, include=include, computed=computed,
                                     allow_cycles=allow_cycles, sort_alphabetically=sort_alphabetically)
